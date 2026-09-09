"use client";

import { EvaluationPreviewResponse } from "@/types/evaluation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { CheckCircle2, XCircle, AlertCircle, Lightbulb } from "lucide-react";
import { cn } from "@/lib/utils";

function getScoreColor(score: number) {
  if (score >= 80) return "text-green-600 dark:text-green-400";
  if (score >= 60) return "text-amber-600 dark:text-amber-400";
  return "text-red-600 dark:text-red-400";
}

function getScoreBg(score: number) {
  if (score >= 80) return "bg-green-100 dark:bg-green-900/30";
  if (score >= 60) return "bg-amber-100 dark:bg-amber-900/30";
  return "bg-red-100 dark:bg-red-900/30";
}

export function EvaluationResultView({ result }: { result: EvaluationPreviewResponse }) {
  const formatScore = (num: number) => Math.round(num);

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      
      {/* Overall Score */}
      <Card className="border-2 shadow-sm">
        <CardContent className="p-6 flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-muted-foreground uppercase tracking-wider mb-1">Overall Score</p>
            <h2 className="text-3xl font-bold">CF Score</h2>
          </div>
          <div className={cn("w-20 h-20 rounded-full flex items-center justify-center text-3xl font-bold", getScoreBg(result.overall_score), getScoreColor(result.overall_score))}>
            {formatScore(result.overall_score)}
          </div>
        </CardContent>
      </Card>

      {/* Composite Scores */}
      <div className="grid grid-cols-3 gap-4">
        {[
          { label: "Response Quality", score: result.response_quality_score },
          { label: "Objection Handling", score: result.objection_handling_score },
          { label: "Forward Momentum", score: result.forward_momentum_score }
        ].map((item) => (
          <Card key={item.label}>
            <CardContent className="p-4 text-center">
              <p className="text-xs font-medium text-muted-foreground mb-2 line-clamp-1">{item.label}</p>
              <p className={cn("text-2xl font-bold", getScoreColor(item.score))}>{formatScore(item.score)}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Feedback Sections */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card className="border-green-100 dark:border-green-900/30">
          <CardHeader className="p-4 pb-2">
            <CardTitle className="text-sm flex items-center gap-2 text-green-700 dark:text-green-400">
              <CheckCircle2 className="w-4 h-4" /> Strengths
            </CardTitle>
          </CardHeader>
          <CardContent className="p-4 pt-0">
            <ul className="space-y-2">
              {result.strengths?.map((s, i) => (
                <li key={i} className="text-sm flex items-start gap-2">
                  <span className="text-green-500 mt-0.5">•</span>
                  <span>{s}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>

        <Card className="border-red-100 dark:border-red-900/30">
          <CardHeader className="p-4 pb-2">
            <CardTitle className="text-sm flex items-center gap-2 text-red-700 dark:text-red-400">
              <XCircle className="w-4 h-4" /> Weaknesses
            </CardTitle>
          </CardHeader>
          <CardContent className="p-4 pt-0">
            <ul className="space-y-2">
              {result.weaknesses?.map((w, i) => (
                <li key={i} className="text-sm flex items-start gap-2">
                  <span className="text-red-500 mt-0.5">•</span>
                  <span>{w}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>

      <Card className="border-amber-100 dark:border-amber-900/30">
        <CardHeader className="p-4 pb-2">
          <CardTitle className="text-sm flex items-center gap-2 text-amber-700 dark:text-amber-400">
            <AlertCircle className="w-4 h-4" /> Missed Opportunities
          </CardTitle>
        </CardHeader>
        <CardContent className="p-4 pt-0">
          <ul className="space-y-2">
            {result.missed_opportunities?.map((m, i) => (
              <li key={i} className="text-sm flex items-start gap-2">
                <span className="text-amber-500 mt-0.5">•</span>
                <span>{m}</span>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>

      <Card className="border-blue-100 dark:border-blue-900/30 bg-blue-50/50 dark:bg-blue-900/10">
        <CardHeader className="p-4 pb-2">
          <CardTitle className="text-sm flex items-center gap-2 text-blue-700 dark:text-blue-400">
            <Lightbulb className="w-4 h-4" /> Recommended Strategy
          </CardTitle>
        </CardHeader>
        <CardContent className="p-4 pt-0">
          <p className="text-sm">{result.recommended_strategy}</p>
        </CardContent>
      </Card>

      {/* Dimensions */}
      <div>
        <h3 className="font-semibold text-lg mb-4">Dimension Breakdown</h3>
        <div className="space-y-3">
          {result.dimensions?.map((dim) => {
            const percentage = (dim.score / 5.0) * 100;
            return (
              <div key={dim.dimension} className="bg-card border rounded-md p-3">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium capitalize">{dim.dimension.replace('_', ' ')}</span>
                  <span className="text-sm font-bold">{dim.score.toFixed(1)} / 5</span>
                </div>
                <Progress value={percentage} className={cn("h-2 mb-2", 
                  percentage >= 80 ? "[&>div]:bg-green-500" : 
                  percentage >= 60 ? "[&>div]:bg-amber-500" : "[&>div]:bg-red-500"
                )} />
                <p className="text-xs text-muted-foreground mt-2">{dim.reasoning}</p>
              </div>
            );
          })}
        </div>
      </div>

    </div>
  );
}
