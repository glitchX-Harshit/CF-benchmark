import { Button } from "@/components/ui/button";
import Link from "next/link";
import { ArrowRight, BarChart2, ShieldCheck, Zap } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] text-center px-4">
      <div className="max-w-3xl space-y-8">
        <h1 className="text-5xl font-extrabold tracking-tight sm:text-6xl text-slate-900 dark:text-white">
          Measure Sales Response Quality with <span className="text-blue-600">Precision</span>
        </h1>
        <p className="text-xl text-muted-foreground leading-relaxed">
          CF Benchmark provides deterministic, explainable scoring for your sales team's responses. Stop guessing and start measuring objection handling, forward momentum, and response quality.
        </p>
        <div className="flex items-center justify-center gap-4 pt-4">
          <Button asChild size="lg" className="h-12 px-8 text-base">
            <Link href="/evaluate">
              Try the Playground
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg" className="h-12 px-8 text-base">
            <Link href="/dashboard">View Dashboard</Link>
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 pt-16 text-left">
          <div className="space-y-3">
            <div className="h-12 w-12 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400">
              <ShieldCheck className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-semibold">Deterministic Scoring</h3>
            <p className="text-muted-foreground">Consistent, reliable evaluation criteria that removes subjectivity from quality assurance.</p>
          </div>
          <div className="space-y-3">
            <div className="h-12 w-12 rounded-lg bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center text-amber-600 dark:text-amber-400">
              <BarChart2 className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-semibold">Explainable Feedback</h3>
            <p className="text-muted-foreground">Detailed breakdowns of strengths, weaknesses, and missed opportunities for every response.</p>
          </div>
          <div className="space-y-3">
            <div className="h-12 w-12 rounded-lg bg-green-100 dark:bg-green-900/30 flex items-center justify-center text-green-600 dark:text-green-400">
              <Zap className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-semibold">Benchmark Comparison</h3>
            <p className="text-muted-foreground">See how your team's responses stack up against industry standards and top performers.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
