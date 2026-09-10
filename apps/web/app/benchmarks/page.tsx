"use client";

import { useState, useEffect } from "react";

export default function BenchmarkPage() {
  const [scenarios, setScenarios] = useState<any[]>([]);
  const [selectedScenario, setSelectedScenario] = useState<any | null>(null);
  const [response, setResponse] = useState("");
  const [evaluation, setEvaluation] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/benchmarks/scenarios")
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
    <div className="p-8 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold tracking-tight mb-8">CF Benchmark Test</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="bg-white p-6 border border-gray-200 rounded-xl shadow-sm">
            <h2 className="font-semibold mb-4">Select Scenario</h2>
            <select 
              className="w-full border border-gray-300 rounded-md p-2"
              onChange={(e) => setSelectedScenario(scenarios.find(s => s.id === e.target.value))}
              value={selectedScenario?.id || ""}
            >
              {scenarios.map(s => (
                <option key={s.id} value={s.id}>{s.name} ({s.category})</option>
              ))}
            </select>

            {selectedScenario && (
              <div className="mt-6 space-y-4 text-sm">
                <div>
                  <span className="font-medium text-gray-500">Prospect: </span>
                  {selectedScenario.prospect_context.role} | {selectedScenario.prospect_context.industry}
                </div>
                <div>
                  <span className="font-medium text-gray-500">Context: </span>
                  {selectedScenario.conversation_context.stage} stage. Pain: {selectedScenario.conversation_context.pain_points.join(", ")}
                </div>
                <div className="bg-red-50 text-red-900 p-4 rounded-lg mt-4 border border-red-100">
                  <span className="font-semibold">Objection: </span>
                  "{selectedScenario.objection.text}"
                </div>
              </div>
            )}
          </div>

          <div className="bg-white p-6 border border-gray-200 rounded-xl shadow-sm">
            <h2 className="font-semibold mb-4">Seller Response</h2>
            <textarea
              className="w-full border border-gray-300 rounded-md p-3 h-40"
              placeholder="Type your response to the objection..."
              value={response}
              onChange={(e) => setResponse(e.target.value)}
            />
            <button
              onClick={handleEvaluate}
              disabled={loading || !response}
              className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-md font-medium hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? "Evaluating..." : "Run Evaluation"}
            </button>
          </div>
        </div>

        <div>
          {evaluation && (
            <div className="bg-white p-6 border border-gray-200 rounded-xl shadow-sm h-full">
              <h2 className="text-xl font-bold mb-6">Evaluation Result</h2>
              
              <div className="mb-8 text-center">
                <div className="text-5xl font-extrabold text-blue-600">
                  {evaluation.overall_score.toFixed(1)}
                  <span className="text-2xl text-gray-400">/100</span>
                </div>
                <div className="text-gray-500 font-medium mt-2">Overall Score</div>
              </div>

              <div className="space-y-4 mb-8">
                <h3 className="font-semibold text-gray-700 border-b pb-2">Rubrics</h3>
                {Object.values(evaluation.result.rubrics).map((r: any) => (
                  <div key={r.rubric_id} className="flex justify-between items-center text-sm">
                    <span className="capitalize">{r.rubric_id.replace("_", " ")}</span>
                    <span className="font-medium">{r.score} / {r.max_score}</span>
                  </div>
                ))}
              </div>

              <div className="space-y-4">
                <h3 className="font-semibold text-gray-700 border-b pb-2">Feedback</h3>
                <div>
                  <h4 className="text-sm font-medium text-green-700">Strengths</h4>
                  <ul className="list-disc pl-5 text-sm text-gray-600">
                    {evaluation.result.strengths.map((s: string, i: number) => <li key={i}>{s}</li>)}
                  </ul>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-red-700">Weaknesses</h4>
                  <ul className="list-disc pl-5 text-sm text-gray-600">
                    {evaluation.result.weaknesses.map((s: string, i: number) => <li key={i}>{s}</li>)}
                  </ul>
                </div>
              </div>
              
              <div className="mt-8 text-xs text-gray-400 text-center">
                Evaluator: {evaluation.result.evaluator_version}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
