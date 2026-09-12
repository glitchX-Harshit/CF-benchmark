import os
import re
import time
from typing import Dict, Any, List, Optional
from cf_engine.models.cold_call import (
    ConversationInput, CFReport, LikelyProspectEffect,
    LikelyReaction, DirectionItem, OpportunitySurface, RiskItem,
    ResponseCost, FinalGrade, OpportunityItem, CFReportMetadata
)
from cf_engine.llm.providers import GeminiProvider, OpenAIProvider
from cf_engine.llm.schemas import SemanticSignals
from cf_engine.evaluators.semantic_evaluator import calculate_deterministic_score

class ColdCallEngine:
    """
    Deterministic evaluation engine with LLM semantic layer.
    """
    
    def __init__(self):
        llm_provider = os.environ.get("CF_LLM_PROVIDER", "gemini").lower()
        if llm_provider == "openai":
            self.llm = OpenAIProvider()
        else:
            self.llm = GeminiProvider()
            
    def _get_llm_signals_with_fallback(self, conversation: dict, seller_response: str, objective_signals: dict) -> tuple[Optional[SemanticSignals], CFReportMetadata]:
        is_llm_enabled = os.environ.get("CF_LLM_ENABLED", "false").lower() == "true"
        
        metadata = CFReportMetadata(analysis_mode="hybrid", semantic_source="llm", llm_used=True, fallback_used=False)
        
        if not is_llm_enabled:
            metadata.analysis_mode = "deterministic_fallback"
            metadata.semantic_source = "deterministic_fallback"
            metadata.llm_used = False
            metadata.fallback_used = True
            return None, metadata
            
        max_retries = int(os.environ.get("CF_LLM_MAX_RETRIES", "2"))
        
        for attempt in range(max_retries + 1):
            try:
                signals = self.llm.interpret_response(
                    conversation_context=conversation,
                    seller_response=seller_response,
                    objective_signals=objective_signals
                )
                return signals, metadata
            except Exception as e:
                import requests
                # Check for quota/rate limit errors
                if isinstance(e, requests.exceptions.HTTPError):
                    if e.response.status_code in [429, 403]:
                        raise RuntimeError("LLM_QUOTA_REACHED")
                
                # Log the exception locally if needed
                print(f"LLM API Error: {e}")
                if attempt == max_retries:
                    break
                time.sleep(1) # simple backoff
                
        # If we failed all retries for non-quota reasons
        metadata.analysis_mode = "deterministic_fallback"
        metadata.semantic_source = "deterministic_fallback"
        metadata.fallback_used = True
        return None, metadata
        
    def evaluate(self, conversation: ConversationInput, seller_response: str, use_llm: bool = False) -> CFReport:
        # Phase 1: Parsing & Cost (Deterministic)
        word_count = len(seller_response.split())
        estimated_seconds = round(word_count / 2.5, 1)
        question_count = seller_response.count("?")
        
        cognitive_load = min(100, word_count + (question_count * 15))
        conversational_cost = min(100, (word_count * 1.5) + (question_count * 10))
        
        response_cost = ResponseCost(
            word_count=word_count,
            estimated_seconds=estimated_seconds,
            cognitive_load=int(cognitive_load),
            conversational_cost=int(conversational_cost)
        )
        
        contains_placeholders = bool(re.search(r'\[.*?\]', seller_response))
        contains_percentage = bool(re.search(r'\b\d+\s*%', seller_response)) or "percent" in seller_response.lower()
        contains_meeting_request = any(w in seller_response.lower() for w in ["minutes", "meeting", "chat", "discuss", "next tuesday", "tomorrow", "next week"])
        contains_financial_reframing = any(w in seller_response.lower() for w in ["roi", "savings", "revenue", "budget back", "pay for itself"])

        objective_signals = {
            "word_count": word_count,
            "question_count": question_count,
            "estimated_seconds": estimated_seconds,
            "contains_question": question_count > 0,
            "contains_product_pitch": any(w in seller_response.lower() for w in ["platform", "solution", "integrate", "powered", "feature", "analytics", "much more"]),
            "contains_acknowledgement_phrase": any(w in seller_response.lower() for w in ["got it", "makes sense", "understood", "okay", "i hear you"]),
            "contains_placeholders": contains_placeholders,
            "contains_percentage": contains_percentage,
            "contains_meeting_request": contains_meeting_request,
            "contains_financial_reframing": contains_financial_reframing
        }
        
        metadata = CFReportMetadata(analysis_mode="deterministic", semantic_source="deterministic", llm_used=False, fallback_used=False)
        semantic = None
        
        # Override to enable LLM if requested via API config, but only if we have an API key or env says yes
        if use_llm:
            os.environ["CF_LLM_ENABLED"] = "true"
            conv_dict = conversation.model_dump()
            semantic, metadata = self._get_llm_signals_with_fallback(conv_dict, seller_response, objective_signals)

        # Base heuristics for fallback
        is_pitch = objective_signals["contains_product_pitch"]
        is_short = word_count < 20
        is_long = word_count > 40
        is_acknowledgement = objective_signals["contains_acknowledgement_phrase"]
        has_question = objective_signals["contains_question"]
        has_multiple_questions = question_count > 1

        if semantic and metadata.analysis_mode == "hybrid":
            # Phase 2 (Hybrid): Deterministic scoring via LLM semantic signals
            scores = calculate_deterministic_score(objective_signals, semantic)
            response_quality_score = scores["response_quality_score"]
            strategic_opportunity_score = scores["strategic_opportunity_score"]
            conversation_direction_score = scores["conversation_direction_score"]
            
            # Map semantic risk triggers
            risks = [RiskItem(type="Detected Risk", severity="high" if r in ["rejection", "shutdown"] else "medium", reason=r) for r in semantic.risk_triggers]
            if objective_signals.get("contains_placeholders"):
                risks.append(RiskItem(type="Credibility Risk", severity="high", reason="Contains template placeholders"))
            
            opened = []
            missed = []
            for opp in semantic.opportunities:
                if opp.evidence_status in ["confirmed_by_prospect", "created_by_response"]:
                    opened.append(OpportunityItem(type=opp.type, strength=80, reason=f"Status: {opp.evidence_status}", reachable_direction="positive"))
                else:
                    missed.append(OpportunityItem(type=opp.type, strength=30, reason=f"Status: {opp.evidence_status}", reachable_direction="neutral"))
            
            eff_eng = "HIGH" if semantic.likely_prospect_state in ["interested", "engaged"] else "MEDIUM" if semantic.likely_prospect_state in ["curious", "neutral"] else "LOW"
            eff_cur = "HIGH" if semantic.likely_prospect_state in ["curious"] else "LOW" if semantic.likely_prospect_state in ["defensive", "dismissive"] else "MEDIUM"
            eff_res = "HIGH" if semantic.likely_prospect_state in ["defensive", "skeptical", "dismissive"] else "LOW"
            eff_tru = "HIGH" if semantic.likely_prospect_state in ["engaged", "interested"] else "LOW" if semantic.likely_prospect_state in ["defensive", "dismissive"] else "MEDIUM"
            eff_rel = "HIGH" if semantic.asks_relevant_discovery else "MEDIUM"
            eff_con = "HIGH" if semantic.creates_continuation_opening else "LOW"
            
            reaction_label = "Likely " + semantic.likely_prospect_state.capitalize()
            reaction_expl = "Based on semantic evaluation."
            
            # Use semantic fields for some cost overwriting if confident
            if semantic.cognitive_load == "low": response_cost.cognitive_load = min(response_cost.cognitive_load, 30)
            elif semantic.cognitive_load == "high": response_cost.cognitive_load = max(response_cost.cognitive_load, 70)

            possible_directions = []
            for op in opened:
                possible_directions.append(DirectionItem(direction=f"Prospect may explore: {op.type}", likelihood_tendency="HIGH", explanation="Opportunity created."))

            for risk in semantic.risk_triggers:
                possible_directions.append(DirectionItem(direction=f"Prospect may disengage due to: {risk}", likelihood_tendency="LOW", explanation="Risk introduced."))
            if not possible_directions:
                possible_directions.append(DirectionItem(direction="Conversation continues neutrally.", likelihood_tendency="MEDIUM", explanation="No strong signals."))
                
        else:
            # Phase 2 (Deterministic): Directional scoring based on specs
            response_quality_score = 50
            strategic_opportunity_score = 50
            conversation_direction_score = 0
            
            # Apply heuristics
            if is_acknowledgement:
                response_quality_score += 10
                
            if is_short and has_question and not is_pitch:
                response_quality_score += 20
                strategic_opportunity_score += 30
                conversation_direction_score += 50
            elif is_pitch and is_long:
                response_quality_score -= 20
                strategic_opportunity_score -= 20
                conversation_direction_score -= 50
            elif is_short and not has_question:
                response_quality_score += 10
                strategic_opportunity_score -= 30
                conversation_direction_score -= 10
            elif is_acknowledgement and not has_question and has_multiple_questions:
                conversation_direction_score -= 20
                
            # Opportunities
            opened = []
            if has_question and not is_pitch:
                opened.append(OpportunityItem(type="Current situation discussion", strength=80, reason="Open question allows prospect to elaborate.", reachable_direction="positive"))
                opened.append(OpportunityItem(type="Workflow discussion", strength=85, reason="Relevant to current tools or processes.", reachable_direction="positive"))
                opened.append(OpportunityItem(type="Potential pain discovery", strength=70, reason="Allows revealing gaps.", reachable_direction="positive"))
                opened.append(OpportunityItem(type="Gap identification", strength=70, reason="Gaps might be shown.", reachable_direction="positive"))

            if is_pitch:
                opened.append(OpportunityItem(type="Rejection", strength=90, reason="Premature pitch triggers resistance.", reachable_direction="negative"))

            missed = []
            risks = []
            if is_pitch:
                risks.append(RiskItem(type="Premature pitching", severity="high", reason="High cognitive load and unearned pitch."))
            if has_multiple_questions:
                risks.append(RiskItem(type="Cognitive overload", severity="medium", reason="Multiple questions can overwhelm."))
            if not is_pitch and has_question:
                risks.append(RiskItem(type="Neutral response risk", severity="low", reason="If the prospect is genuinely satisfied, the conversation may remain neutral."))

            if conversation_direction_score >= 50:
                reaction_label = "Likely engaged"
                reaction_expl = "The response is short, relevant and easy to answer."
                eff_eng, eff_cur, eff_res, eff_tru, eff_rel, eff_con = "HIGH", "MEDIUM", "LOW", "MEDIUM", "HIGH", "HIGH"
            elif conversation_direction_score <= -50:
                reaction_label = "Likely Defensive"
                reaction_expl = "Too much information or unearned pitch creates resistance."
                eff_eng, eff_cur, eff_res, eff_tru, eff_rel, eff_con = "LOW", "LOW", "HIGH", "LOW", "LOW", "LOW"
            else:
                reaction_label = "Likely Neutral"
                reaction_expl = "Does not create strong progression or strong resistance."
                eff_eng, eff_cur, eff_res, eff_tru, eff_rel, eff_con = "MEDIUM", "LOW", "LOW", "MEDIUM", "MEDIUM", "MEDIUM"

            obj = conversation.current_state.objection if conversation.current_state and conversation.current_state.objection else "the objection"
            role = conversation.current_state.prospect_role if conversation.current_state and conversation.current_state.prospect_role else "Prospect"
            
            possible_directions=[
                DirectionItem(direction=f"{role} answers the seller's question.", likelihood_tendency="HIGH", explanation="If the question is relevant and easy to answer."),
                DirectionItem(direction=f"{role} reiterates concern about {obj}.", likelihood_tendency="MEDIUM", explanation="If the response didn't reduce resistance."),
                DirectionItem(direction=f"{role} asks for clarification.", likelihood_tendency="MEDIUM", explanation="If the response was confusing or introduced new concepts."),
                DirectionItem(direction=f"{role} gives a short dismissal.", likelihood_tendency="LOW", explanation="If they remain busy or defensive."),
                DirectionItem(direction="Conversation can move toward a workflow or gap discussion.", likelihood_tendency="MEDIUM", explanation="If the prospect engages with the response.")
            ]

        # Common Bounds Check
        response_quality_score = max(0, min(100, response_quality_score))
        strategic_opportunity_score = max(0, min(100, strategic_opportunity_score))
        conversation_direction_score = max(-100, min(100, conversation_direction_score))
        
        # Label generation
        if conversation_direction_score >= 76:
            dir_label = "Strongly Forward-Leaning"
        elif conversation_direction_score >= 51:
            dir_label = "Forward-Leaning"
        elif conversation_direction_score >= 26:
            dir_label = "Moderately Forward"
        elif conversation_direction_score >= 1:
            dir_label = "Slightly Forward"
        elif conversation_direction_score == 0:
            dir_label = "Neutral"
        elif conversation_direction_score >= -25:
            dir_label = "Slightly Negative"
        elif conversation_direction_score >= -50:
            dir_label = "Moderately Negative"
        elif conversation_direction_score >= -75:
            dir_label = "Resistance-Leaning"
        else:
            dir_label = "Strongly Rejection-Leaning"
            
        # Final grade based on spec inputs
        final_cf_score = int(
            (response_quality_score * 0.35) + 
            (strategic_opportunity_score * 0.35) + 
            (((conversation_direction_score + 100) / 2) * 0.30)
        )
        
        if final_cf_score >= 90: grade = "A+"
        elif final_cf_score >= 85: grade = "A"
        elif final_cf_score >= 80: grade = "A-"
        elif final_cf_score >= 75: grade = "B+"
        elif final_cf_score >= 70: grade = "B"
        elif final_cf_score >= 65: grade = "B-"
        elif final_cf_score >= 60: grade = "C+"
        elif final_cf_score >= 50: grade = "C"
        elif final_cf_score >= 35: grade = "D"
        else: grade = "F"
        
        # Visual
        norm = int((conversation_direction_score + 100) / 200 * 24)
        visual = "REJECTION " + "-" * norm + "o" + "-" * (24 - norm) + " PROGRESSION"

        # Verdict logic
        has_high_risk = any(r.severity == "high" for r in risks) if 'risks' in locals() else False
        
        if conversation_direction_score >= 70:
            if has_high_risk:
                verdict = "The response creates strategic progression, but contains major high-severity risks that threaten the conversation."
            else:
                verdict = "Strong cold-call response. It creates multiple useful paths without forcing a pitch or adding unnecessary conversational cost."
        elif conversation_direction_score >= 30:
            verdict = "The response generally supports progression but has identifiable weaknesses."
        elif conversation_direction_score >= -20:
            verdict = "The response keeps the conversation alive but creates limited strategic movement."
        elif conversation_direction_score >= -60:
            verdict = "Creates resistance. The prospect may disengage due to friction."
        else:
            verdict = "Highly likely to shorten or damage the conversation. Specific rejection triggers detected."

        # Hashing and Logging
        import hashlib
        import json
        import logging
        
        logger = logging.getLogger("cf_engine")
        
        sig_dump = semantic.model_dump_json() if semantic else "{}"
        obj_text = json.dumps(conversation.current_state.model_dump() if conversation.current_state else {})
        raw_str = f"{obj_text}_{seller_response}_{sig_dump}"
        content_hash = hashlib.sha256(raw_str.encode('utf-8')).hexdigest()[:12]
        
        logger.info(f"--- CF Engine Run [{content_hash}] ---")
        logger.info(f"Mode: {metadata.analysis_mode}")
        logger.info(f"Scores: Quality={response_quality_score}, Strategic={strategic_opportunity_score}, Direction={conversation_direction_score}")
        logger.info(f"Final Score: {final_cf_score}")
        logger.info(f"Normalized Signals: {sig_dump}")

        return CFReport(
            seller_response=seller_response,
            response_quality={"score": int(response_quality_score), "label": "Measured Quality"},
            strategic_opportunity={"score": int(strategic_opportunity_score), "label": "Measured Opportunity"},
            conversation_direction={"score": int(conversation_direction_score), "label": dir_label},
            direction_visual=visual,
            likely_prospect_effect=LikelyProspectEffect(
                engagement=eff_eng,
                curiosity=eff_cur,
                resistance=eff_res,
                trust=eff_tru,
                relevance=eff_rel,
                continuation=eff_con
            ),
            likely_reaction=LikelyReaction(label=reaction_label, explanation=reaction_expl),
            possible_directions=possible_directions,
            opportunity_surface=OpportunitySurface(opened=opened, missed=missed, weakened=[]),
            risks=risks,
            response_cost=response_cost,
            resilience={"score": 75, "explanation": "General resilience estimate"},
            final=FinalGrade(
                cf_grade=grade,
                cf_score=final_cf_score,
                direction=dir_label,
                verdict=verdict
            ),
            metadata=metadata
        )
