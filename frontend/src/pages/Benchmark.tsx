import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle2, AlertCircle, User, Sparkles, ChevronDown, Check } from "lucide-react";

function DirectionGraph({ score = 62, compact = false }: { score?: number; compact?: boolean }) {
  const points = compact
    ? "8,92 42,76 74,81 108,52 142,61 176,28 210,38"
    : "8,118 54,100 96,108 138,73 180,84 222,44 264,58 308,20";

  return (
    <div className={`direction-graph ${compact ? "direction-graph--compact" : ""}`}>
      <div className="direction-graph__topline">
        <span>{compact ? "LIVE SIGNAL PATH" : "DIRECTION / RESPONSE MOMENTUM"}</span>
        <strong>{score}<small>/100</small></strong>
      </div>
      <svg viewBox="0 0 316 132" role="img" aria-label="Response direction graph">
        <line x1="8" y1="118" x2="308" y2="118" className="direction-graph__axis" />
        <line x1="8" y1="78" x2="308" y2="78" className="direction-graph__grid" />
        <line x1="8" y1="38" x2="308" y2="38" className="direction-graph__grid" />
        <polyline points={points} className="direction-graph__line" />
        {points.split(" ").map((point, index) => {
          const [cx, cy] = point.split(",");
          return <circle key={point} cx={cx} cy={cy} r={index === points.split(" ").length - 1 ? 4 : 2.5} className="direction-graph__point" />;
        })}
      </svg>
      <div className="direction-graph__labels"><span>OPEN</span><span>UNCERTAIN</span><span>MOVE FORWARD</span></div>
    </div>
  );
}

export default function BenchmarkPage() {
  const [scenarios, setScenarios] = useState<any[]>([]);
  const [selectedScenario, setSelectedScenario] = useState<any | null>(null);
  const [response, setResponse] = useState("");
  const [evaluation, setEvaluation] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [scenarioMenuOpen, setScenarioMenuOpen] = useState(false);

  useEffect(() => {
    fetch("/api/v1/benchmarks/scenarios")
      .then(res => res.json())
      .then(data => {
        setScenarios(data);
        if (data.length > 0) setSelectedScenario(data[0]);
      })
      .catch(err => console.error("Failed to load scenarios:", err));
  }, []);

  const handleEvaluate = async () => {
    if (!selectedScenario || !response) return;
    setLoading(true);
    setEvaluation(null);

    try {
      const res = await fetch("/api/v1/evaluate/cold-call", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation: {
            current_state: {
              prospect_role: selectedScenario.prospect_context.role || "",
              stage: "objection",
              objection: selectedScenario.objection.text,
              engagement_level: "medium",
              resistance_level: "medium"
            },
            previous_messages: []
          },
          seller_response: response,
          use_llm: true
        })
      });
      const data = await res.json();
      setEvaluation(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-7xl mx-auto space-y-10"
    >
      <header className="benchmark-header mb-10">
        <div className="benchmark-header__visual" aria-hidden="true">
          <span className="benchmark-header__cross">+</span>
          <span className="benchmark-header__ring" />
          <span className="benchmark-header__figure"><i /><b /><em /></span>
          <span className="benchmark-header__label">SIGNAL / DIRECTION / NEXT MOVE</span>
        </div>
        <div className="benchmark-header__copy">
          <p className="eyebrow"><span className="eyebrow__line" /> CF Benchmark / 02</p>
        <h1 className="text-5xl font-black tracking-tight mb-4 text-[#171717]">
          Response review
        </h1>
        <p className="text-[#6d6a63] text-lg max-w-2xl mx-auto">
          Evaluate seller responses against dynamic scenarios. Upload transcripts or type directly to analyze objection handling and performance.
        </p>
        </div>
      </header>

      <div className="grid grid-cols-1 xl:grid-cols-12 gap-8">
        
        {/* Left Column: Inputs */}
        <div className="xl:col-span-6 space-y-6">
          
          {/* Scenario Selector */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="p-8 rounded-none bg-[#f4f0e7] border border-[#171717]/20"
          >
            <div className="panel-kicker">01 / Choose a scenario</div>
            <h2 className="text-xl font-bold mb-6 flex items-center gap-3">
              <span className="w-8 h-8 rounded-full bg-[#5b3bc4] text-white flex items-center justify-center text-sm">1</span>
              Configure Scenario
            </h2>
            
            <div className="scenario-picker">
              <button
                type="button"
                className={`scenario-picker__trigger ${scenarioMenuOpen ? "is-open" : ""}`}
                onClick={() => setScenarioMenuOpen((open) => !open)}
                aria-expanded={scenarioMenuOpen}
                aria-haspopup="listbox"
              >
                <span className="scenario-picker__meta">Selected scenario</span>
                <span className="scenario-picker__value">
                  <span>{selectedScenario?.name || "Loading scenarios..."}</span>
                  <small>{selectedScenario?.category || "Please wait"}</small>
                </span>
                <ChevronDown size={18} />
              </button>
              <AnimatePresence>
                {scenarioMenuOpen && (
                  <motion.div
                    className="scenario-picker__menu"
                    initial={{ opacity: 0, y: -8, scale: .98 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: -8, scale: .98 }}
                    transition={{ duration: .16 }}
                    role="listbox"
                  >
                    <div className="scenario-picker__menu-label">Available compositions</div>
                    {scenarios.map((scenario, index) => {
                      const isSelected = scenario.id === selectedScenario?.id;
                      return (
                        <button
                          type="button"
                          key={scenario.id}
                          className={`scenario-option ${isSelected ? "is-selected" : ""}`}
                          onClick={() => {
                            setSelectedScenario(scenario);
                            setScenarioMenuOpen(false);
                          }}
                          role="option"
                          aria-selected={isSelected}
                        >
                          <span className="scenario-option__index">0{index + 1}</span>
                          <span className="scenario-option__copy"><strong>{scenario.name}</strong><small>{scenario.category}</small></span>
                          {isSelected && <Check size={16} />}
                        </button>
                      );
                    })}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {selectedScenario && (
              <AnimatePresence mode="wait">
                <motion.div 
                  key={selectedScenario.id}
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  className="mt-6 overflow-hidden"
                >
                  <div className="p-6 rounded-none bg-[#dfe5f0] border border-[#171717]/15 space-y-4">
                    <div className="flex gap-4 items-start">
                      <div className="mt-1 p-2 rounded-none bg-[#b6c7e8] text-[#171717]"><User className="w-4 h-4" /></div>
                      <div className="w-full">
                        <div className="text-xs text-[#6d6a63] uppercase tracking-wider font-semibold mb-1">Prospect (Editable)</div>
                        <div className="flex items-center">
                          <input 
                            value={selectedScenario.prospect_context.role || ""} 
                            onChange={e => setSelectedScenario({...selectedScenario, prospect_context: {...selectedScenario.prospect_context, role: e.target.value}})}
                            className="text-sm font-medium bg-transparent border-b border-transparent hover:border-[#171717]/30 focus:border-[#5b3bc4] outline-none w-auto max-w-[150px] transition-colors"
                          />
                          <span className="text-sm font-medium mx-2">•</span>
                          <input 
                            value={selectedScenario.prospect_context.industry || ""} 
                            onChange={e => setSelectedScenario({...selectedScenario, prospect_context: {...selectedScenario.prospect_context, industry: e.target.value}})}
                            className="text-sm font-medium bg-transparent border-b border-transparent hover:border-[#171717]/30 focus:border-[#5b3bc4] outline-none w-auto transition-colors"
                          />
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex gap-4 items-start">
                      <div className="mt-1 p-2 rounded-none bg-[#b6c7e8] text-[#171717]"><AlertCircle className="w-4 h-4" /></div>
                      <div className="w-full">
                        <div className="text-xs text-[#6d6a63] uppercase tracking-wider font-semibold mb-1">Context (Editable)</div>
                        <div className="flex items-center">
                          <input 
                            value={selectedScenario.conversation_context.stage || ""} 
                            onChange={e => setSelectedScenario({...selectedScenario, conversation_context: {...selectedScenario.conversation_context, stage: e.target.value}})}
                            className="text-sm font-medium bg-transparent border-b border-transparent hover:border-[#171717]/30 focus:border-[#5b3bc4] outline-none w-auto max-w-[100px] transition-colors"
                          />
                          <span className="text-sm font-medium mx-2">stage • Pain:</span>
                          <input 
                            value={selectedScenario.conversation_context.pain_points.join(", ")} 
                            onChange={e => setSelectedScenario({...selectedScenario, conversation_context: {...selectedScenario.conversation_context, pain_points: e.target.value.split(", ")}})}
                            className="text-sm font-medium bg-transparent border-b border-transparent hover:border-[#171717]/30 focus:border-[#5b3bc4] outline-none flex-1 transition-colors"
                          />
                        </div>
                      </div>
                    </div>

                    <div className="mt-6 p-5 rounded-none bg-[#d9c5d3] border-l-4 border-[#5b3bc4]">
                      <div className="text-xs text-[#5b3bc4] uppercase tracking-wider font-bold mb-2">The Objection (Editable)</div>
                      <textarea 
                        value={selectedScenario.objection.text}
                        onChange={e => setSelectedScenario({...selectedScenario, objection: {...selectedScenario.objection, text: e.target.value}})}
                        className="text-lg font-medium text-[#171717] italic bg-transparent border border-transparent hover:border-[#5b3bc4]/30 focus:border-[#5b3bc4] outline-none w-full resize-none min-h-[80px] p-2 transition-colors rounded-sm"
                      />
                    </div>
                  </div>
                </motion.div>
              </AnimatePresence>
            )}
          </motion.div>

          {/* Input Area */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="p-8 rounded-none bg-[#f4f0e7] border border-[#171717]/20"
          >
            <div className="panel-kicker">02 / Add a response</div>
            <h2 className="text-xl font-bold mb-6 flex items-center gap-3">
              <span className="w-8 h-8 rounded-full bg-[#5b3bc4] text-white flex items-center justify-center text-sm">2</span>
              Provide Response
            </h2>

            <div className="relative">
              <textarea
                className="w-full bg-[#dfe5f0] border border-[#171717]/30 rounded-none p-6 text-[#171717] placeholder-[#6d6a63] focus:outline-none focus:ring-2 focus:ring-[#5b3bc4] transition-shadow min-h-[200px] resize-y"
                placeholder="Type the seller's response here..."
                value={response}
                onChange={(e) => setResponse(e.target.value)}
              />
            </div>

            <button
              onClick={handleEvaluate}
              disabled={loading || !response}
              className="mt-8 w-full py-5 rounded-none font-bold text-lg flex items-center justify-center gap-3 transition-all relative overflow-hidden group disabled:opacity-50 disabled:cursor-not-allowed bg-[#5b3bc4] text-white hover:bg-[#3157a4]"
            >
              <span className="relative z-10 flex items-center gap-2">
                {loading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Run benchmark
                  </>
                )}
              </span>
            </button>
          </motion.div>
        </div>

        {/* Right Column: Results */}
        <div className="xl:col-span-6 relative">
          <div className="sticky top-10">
            <AnimatePresence mode="wait">
              {!evaluation ? (
                <motion.div 
                  key="empty"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="h-[600px] rounded-none border border-[#171717]/25 border-dashed flex flex-col items-center justify-center text-center p-10 bg-[#f4f0e7]"
                >
                  <DirectionGraph compact />
                  <h3 className="text-xl font-bold text-[#171717] mb-2">Map the next move</h3>
                  <p className="text-[#6d6a63]">Add a response and run the benchmark to plot its direction, quality, and opportunity.</p>
                </motion.div>
              ) : evaluation.report ? (
                /* NEW CFREPORT FORMAT */
                <motion.div 
                  key="new-results"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="rounded-none bg-[#f4f0e7] border border-[#171717]/25 overflow-hidden shadow-[8px_8px_0_#b6c7e8]"
                >
                  <div className="p-8 border-b border-[#171717]/20 text-center relative overflow-hidden bg-[#b6c7e8]">
                    <div className="relative z-10">
                      <div className="flex justify-between items-center mb-4">
                        <h3 className="text-[#3157a4] font-medium uppercase tracking-widest text-sm">CF COLD CALL ANALYSIS</h3>
                        <span className="text-xs font-bold px-2 py-1 bg-[#171717]/10 text-[#3157a4] rounded-sm">
                          Analysis: {evaluation.report.metadata?.analysis_mode === "hybrid" ? "Hybrid" : 
                                    evaluation.report.metadata?.analysis_mode === "deterministic_fallback" ? "Deterministic fallback" : 
                                    "Deterministic"}
                        </span>
                      </div>
                      <div className="flex justify-center items-end gap-2 mb-2">
                        <span className="text-7xl font-black text-[#171717]">{evaluation.report.final.cf_grade}</span>
                      </div>
                      <div className="text-[#171717] text-lg font-bold mt-2">Score: {evaluation.report.final.cf_score}/100</div>
                      <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-none bg-[#f4f0e7] text-sm font-medium mt-4">
                        <CheckCircle2 className="w-4 h-4 text-[#3157a4]" />
                        {evaluation.report.final.direction}
                      </div>
                    </div>
                  </div>

                  <div className="p-8 space-y-8 bg-[#dfe5f0] text-sm">
                    <div className="p-4 bg-white border border-[#171717]/20 font-medium">
                       Seller Response: "{evaluation.report.seller_response}"
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-4 bg-[#f4f0e7] border border-[#171717]/10">
                        <div className="text-xs text-[#6d6a63] font-bold mb-1">Response Quality</div>
                        <div className="text-xl font-black text-[#5b3bc4]">{evaluation.report.response_quality.score}/100</div>
                      </div>
                      <div className="p-4 bg-[#f4f0e7] border border-[#171717]/10">
                        <div className="text-xs text-[#6d6a63] font-bold mb-1">Strategic Opportunity</div>
                        <div className="text-xl font-black text-[#5b3bc4]">{evaluation.report.strategic_opportunity.score}/100</div>
                      </div>
                    </div>
                    
                    <div>
                        <div className="text-xs font-bold text-[#6d6a63] mb-2 uppercase">Direction Visual</div>
                        <DirectionGraph score={evaluation.report.final.cf_score} />
                    </div>

                    <div className="p-5 rounded-none bg-[#d9c5d3] border-l-4 border-[#5b3bc4]">
                      <div className="text-xs text-[#5b3bc4] uppercase tracking-wider font-bold mb-2">Likely Reaction</div>
                      <div className="font-bold text-[#171717] mb-1">{evaluation.report.likely_reaction.label}</div>
                      <div className="text-sm text-[#171717] italic">{evaluation.report.likely_reaction.explanation}</div>
                    </div>
                    
                    <div>
                      <h4 className="text-sm font-bold text-[#6d6a63] uppercase tracking-wider mb-4 border-b border-[#171717]/20 pb-2">Possible Directions</h4>
                      <ul className="space-y-3">
                        {evaluation.report.possible_directions.map((d: any, i: number) => (
                          <li key={i} className="flex flex-col border-b border-[#171717]/10 pb-2">
                             <div className="font-bold text-[#171717]">{d.direction}</div>
                             <div className="flex gap-4 mt-1 text-[#6d6a63]">
                                <span>Likelihood: <strong className="text-[#3157a4]">{d.likelihood_tendency}</strong></span>
                                <span>{d.explanation}</span>
                             </div>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-5 bg-emerald-500/5 border border-emerald-500/10">
                        <h4 className="text-xs font-bold text-emerald-600 uppercase tracking-wider mb-3">Opened Opportunities</h4>
                        <ul className="space-y-2">
                          {evaluation.report.opportunity_surface.opened.map((o: any, i: number) => (
                            <li key={i} className="text-sm text-emerald-800 leading-relaxed font-medium">✓ {o.type}</li>
                          ))}
                          {evaluation.report.opportunity_surface.opened.length === 0 && <span className="text-emerald-800/50">None</span>}
                        </ul>
                      </div>
                      <div className="p-5 bg-[#d9c5d3] border border-[#5b3bc4]/25">
                        <h4 className="text-xs font-bold text-[#5b3bc4] uppercase tracking-wider mb-3">Risks</h4>
                        <ul className="space-y-2">
                          {evaluation.report.risks.map((r: any, i: number) => (
                            <li key={i} className="text-sm text-[#5b3bc4] leading-relaxed">△ {r.reason}</li>
                          ))}
                          {evaluation.report.risks.length === 0 && <span className="text-[#5b3bc4]/50">None</span>}
                        </ul>
                      </div>
                    </div>
                    
                    <div className="p-4 bg-white border border-[#171717]/20">
                      <div className="text-xs font-bold text-[#6d6a63] uppercase mb-2">Final Verdict</div>
                      <div className="text-[#171717]">{evaluation.report.final.verdict}</div>
                    </div>
                    
                    <div className="pt-4 border-t border-[#171717]/20 flex justify-between items-center text-xs text-[#6d6a63]">
                        <div>Word Count: {evaluation.report.response_cost.word_count}</div>
                        <div>Cost: {evaluation.report.response_cost.conversational_cost}/100</div>
                        <div>Load: {evaluation.report.response_cost.cognitive_load}/100</div>
                    </div>
                  </div>
                </motion.div>
              ) : (
                /* OLD RESULTS FORMAT FALLBACK IF NEEDED */
                <motion.div 
                  key="results"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="rounded-none bg-[#f4f0e7] border border-[#171717]/25 overflow-hidden shadow-[8px_8px_0_#b6c7e8]"
                >
                  <div className="p-8 border-b border-[#171717]/20 text-center relative overflow-hidden bg-[#b6c7e8]">
                    <div className="relative z-10">
                      <h3 className="text-[#3157a4] font-medium uppercase tracking-widest text-sm mb-4">Overall Score</h3>
                      <div className="flex justify-center items-end gap-2 mb-2">
                        <span className="text-7xl font-black text-[#171717]">{evaluation.overall_score?.toFixed(0) || "0"}</span>
                        <span className="text-3xl text-[#3157a4] font-bold mb-2">/100</span>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

      </div>
    </motion.div>
  );
}
