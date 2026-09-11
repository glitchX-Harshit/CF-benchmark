import { useState, useEffect, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { motion, AnimatePresence } from "framer-motion";
import { FileText, UploadCloud, X, CheckCircle2, AlertCircle, Bot, User, Sparkles, Activity, ChevronRight, ChevronDown, Check } from "lucide-react";

export default function BenchmarkPage() {
  const [scenarios, setScenarios] = useState<any[]>([]);
  const [selectedScenario, setSelectedScenario] = useState<any | null>(null);
  const [response, setResponse] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [evaluation, setEvaluation] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [scenarioMenuOpen, setScenarioMenuOpen] = useState(false);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/benchmarks/scenarios")
      .then(res => res.json())
      .then(data => {
        setScenarios(data);
        if (data.length > 0) setSelectedScenario(data[0]);
      })
      .catch(err => console.error("Failed to load scenarios:", err));
  }, []);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      // Simulate extracting text from file
      const reader = new FileReader();
      reader.onload = () => {
        setResponse(reader.result as string);
      };
      reader.readAsText(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop,
    accept: { 'text/plain': ['.txt'], 'application/pdf': ['.pdf'] },
    maxFiles: 1
  });

  const handleEvaluate = async () => {
    if (!selectedScenario || !response) return;
    setLoading(true);
    setEvaluation(null);

    try {
      const res = await fetch("http://localhost:8000/api/v1/evaluations/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          scenario_id: selectedScenario.id,
          response
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
          <span className="benchmark-header__label">OBSERVE / RESPOND / LEARN</span>
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
        <div className="xl:col-span-7 space-y-6">
          
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
                      <div>
                        <div className="text-xs text-[#6d6a63] uppercase tracking-wider font-semibold mb-1">Prospect</div>
                        <div className="text-sm font-medium">{selectedScenario.prospect_context.role} • {selectedScenario.prospect_context.industry}</div>
                      </div>
                    </div>
                    
                    <div className="flex gap-4 items-start">
                      <div className="mt-1 p-2 rounded-none bg-[#b6c7e8] text-[#171717]"><AlertCircle className="w-4 h-4" /></div>
                      <div>
                        <div className="text-xs text-[#6d6a63] uppercase tracking-wider font-semibold mb-1">Context</div>
                        <div className="text-sm font-medium">{selectedScenario.conversation_context.stage} stage • Pain: {selectedScenario.conversation_context.pain_points.join(", ")}</div>
                      </div>
                    </div>

                    <div className="mt-6 p-5 rounded-none bg-[#d9c5d3] border-l-4 border-[#5b3bc4]">
                      <div className="text-xs text-[#5b3bc4] uppercase tracking-wider font-bold mb-2">The Objection</div>
                      <div className="text-lg font-medium text-[#171717] italic">"{selectedScenario.objection.text}"</div>
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

            {/* Drag and Drop Zone */}
            <div 
              {...getRootProps()} 
              className={`mb-6 p-8 border-2 border-dashed rounded-2xl text-center transition-all cursor-pointer ${
                isDragActive ? "border-[#5b3bc4] bg-[#d3c8eb]/40" : "border-[#171717]/30 hover:border-[#5b3bc4] hover:bg-[#dfe5f0]"
              }`}
            >
              <input {...getInputProps()} />
              <div className="w-16 h-16 mx-auto rounded-none bg-[#b6c7e8] flex items-center justify-center mb-4">
                <UploadCloud className={`w-8 h-8 ${isDragActive ? "text-[#5b3bc4]" : "text-[#6d6a63]"}`} />
              </div>
              <p className="text-lg font-medium mb-2">
                {isDragActive ? "Drop file here" : "Drag & drop transcript"}
              </p>
              <p className="text-[#6d6a63] text-sm">TXT or PDF files supported. Or type directly below.</p>
              
              {file && (
                <div className="mt-6 inline-flex items-center gap-3 px-4 py-2 rounded-none bg-[#171717] text-sm text-[#fffaf0]">
                  <FileText className="w-4 h-4 text-[#b6c7e8]" />
                  {file.name}
                  <button 
                    onClick={(e) => { e.stopPropagation(); setFile(null); setResponse(""); }}
                    className="p-1 hover:bg-white/20 rounded-full transition-colors"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </div>
              )}
            </div>

            <div className="relative">
              <textarea
                className="w-full bg-[#dfe5f0] border border-[#171717]/30 rounded-none p-6 text-[#171717] placeholder-[#6d6a63] focus:outline-none focus:ring-2 focus:ring-[#5b3bc4] transition-shadow min-h-[200px] resize-y"
                placeholder="Type the seller's response here..."
                value={response}
                onChange={(e) => setResponse(e.target.value)}
              />
              <div className="absolute top-6 left-6 -translate-x-12 opacity-50"><Bot className="w-6 h-6" /></div>
            </div>

            <button
              onClick={handleEvaluate}
              disabled={loading || !response}
              className="mt-8 w-full py-5 rounded-none font-bold text-lg flex items-center justify-center gap-3 transition-all relative overflow-hidden group disabled:opacity-50 disabled:cursor-not-allowed bg-[#5b3bc4] text-white hover:bg-[#3157a4]"
            >
              <span className="relative z-10 flex items-center gap-2">
                {loading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-black" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Run                     Run benchmark
                  </>
                )}
              </span>
            </button>
          </motion.div>
        </div>

        {/* Right Column: Results */}
        <div className="xl:col-span-5 relative">
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
                  <div className="w-24 h-24 rounded-none bg-[#b6c7e8] flex items-center justify-center mb-6">
                    <Activity className="w-10 h-10 text-[#3157a4]" />
                  </div>
                  <h3 className="text-xl font-bold text-[#171717] mb-2">Awaiting Input</h3>
                  <p className="text-[#6d6a63]">Add a response and run the benchmark to see the detailed review here.</p>
                </motion.div>
              ) : (
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
                        <span className="text-7xl font-black text-[#171717]">{evaluation.overall_score.toFixed(0)}</span>
                        <span className="text-3xl text-[#3157a4] font-bold mb-2">/100</span>
                      </div>
                      <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-none bg-[#f4f0e7] text-sm font-medium mt-4">
                        <CheckCircle2 className="w-4 h-4 text-[#3157a4]" />
                        Analysis Complete
                      </div>
                    </div>
                  </div>

                  <div className="p-8 space-y-8 bg-[#dfe5f0]">
                    
                    <div>
                      <h4 className="text-sm font-bold text-[#6d6a63] uppercase tracking-wider mb-4 border-b border-[#171717]/20 pb-2">Rubric Breakdown</h4>
                      <div className="space-y-4">
                        {Object.values(evaluation.result.rubrics).map((r: any, i) => (
                          <div key={r.rubric_id} className="group">
                            <div className="flex justify-between items-center mb-2">
                              <span className="font-medium text-[#171717] capitalize">{r.rubric_id.replace("_", " ")}</span>
                              <span className="font-bold text-[#171717]">{r.score} <span className="text-[#6d6a63]">/ {r.max_score}</span></span>
                            </div>
                            <div className="h-2 w-full bg-[#171717]/15 rounded-full overflow-hidden">
                              <motion.div 
                                initial={{ width: 0 }}
                                animate={{ width: `${(r.score / r.max_score) * 100}%` }}
                                transition={{ duration: 1, delay: i * 0.1 }}
                                className="h-full bg-[#5b3bc4] rounded-full"
                              />
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-5 rounded-2xl bg-emerald-500/5 border border-emerald-500/10">
                        <h4 className="text-xs font-bold text-emerald-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                          <CheckCircle2 className="w-4 h-4" /> Strengths
                        </h4>
                        <ul className="space-y-2">
                          {evaluation.result.strengths.map((s: string, i: number) => (
                            <li key={i} className="text-sm text-emerald-100/70 leading-relaxed">{s}</li>
                          ))}
                        </ul>
                      </div>
                      <div className="p-5 rounded-none bg-[#d9c5d3] border border-[#5b3bc4]/25">
                        <h4 className="text-xs font-bold text-[#5b3bc4] uppercase tracking-wider mb-3 flex items-center gap-2">
                          <AlertCircle className="w-4 h-4" /> Weaknesses
                        </h4>
                        <ul className="space-y-2">
                          {evaluation.result.weaknesses.map((s: string, i: number) => (
                            <li key={i} className="text-sm text-[#171717]/70 leading-relaxed">{s}</li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    <div className="pt-6 border-t border-[#171717]/20 flex justify-between items-center">
                      <div className="text-xs text-[#6d6a63] font-mono">
                        Version: {evaluation.result.evaluator_version}
                      </div>
                      <button className="text-sm font-medium text-[#5b3bc4] hover:text-[#3157a4] flex items-center gap-1">
                        Detailed Report <ChevronRight className="w-4 h-4" />
                      </button>
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
