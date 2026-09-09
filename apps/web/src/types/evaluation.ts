/**
 * API contract for an ephemeral evaluation run. Preview results are not
 * persisted, which lets the playground evaluate ad-hoc seller responses.
 */
export interface EvaluationPreviewRequest {
  prospect_context?: string;
  conversation_context?: string;
  objection: string;
  seller_response: string;
  sales_stage: string;
  industry?: string;
  company_context?: string;
}

export interface EvaluationDimensionScore {
  dimension: string;
  score: number;
  reasoning: string;
  /** The API may return one excerpt or a collection of supporting excerpts. */
  evidence: string | string[];
}

export type ConfidenceLevel = "low" | "medium" | "high" | (string & {});

export interface EvaluationPreviewResponse {
  overall_score: number;
  response_quality_score: number;
  objection_handling_score: number;
  forward_momentum_score: number;
  dimensions: EvaluationDimensionScore[];
  strengths: string[];
  weaknesses: string[];
  missed_opportunities: string[];
  recommended_strategy: string;
  confidence_score: number;
  confidence_level: ConfidenceLevel;
  uncertainty_reasons: string[];
}
