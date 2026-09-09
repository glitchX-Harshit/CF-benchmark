"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { EvaluationResultView } from "@/components/evaluation/evaluation-result-view";
import { evaluationApi } from "@/lib/api-client";
import { EvaluationPreviewResponse } from "@/types/evaluation";

const formSchema = z.object({
  objection: z.string().min(10, "Objection must be at least 10 characters"),
  seller_response: z.string().min(10, "Response must be at least 10 characters"),
  sales_stage: z.string().min(1, "Stage is required"),
  industry: z.string().optional(),
});

export default function EvaluatePage() {
  const [result, setResult] = useState<EvaluationPreviewResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      objection: "We are already using Salesforce and don't need another tool.",
      seller_response: "I hear you. Many of our customers use Salesforce. Our tool integrates directly with it to provide better outbound analytics. Have you found Salesforce reporting easy for outbound?",
      sales_stage: "discovery",
      industry: "SaaS",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true);
    try {
      // Provide dummy scenario context for the preview
      const response = await evaluationApi.preview({
        ...values,
      });
      setResult(response);
    } catch (error) {
      console.error(error);
      alert("Failed to evaluate response.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Playground</h1>
        <p className="text-muted-foreground">Test the evaluation engine with ad-hoc responses.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Evaluation Parameters</CardTitle>
            <CardDescription>Enter the prospect's objection and your response.</CardDescription>
          </CardHeader>
          <CardContent>
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                <FormField
                  control={form.control}
                  name="sales_stage"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Sales Stage</FormLabel>
                      <FormControl>
                        <Input placeholder="e.g. Discovery" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="industry"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Industry</FormLabel>
                      <FormControl>
                        <Input placeholder="e.g. SaaS" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="objection"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Prospect Objection</FormLabel>
                      <FormControl>
                        <Textarea placeholder="What did the prospect say?" className="h-24" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="seller_response"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Seller Response</FormLabel>
                      <FormControl>
                        <Textarea placeholder="How did you respond?" className="h-32" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <Button type="submit" disabled={isLoading} className="w-full">
                  {isLoading ? "Evaluating..." : "Evaluate Response"}
                </Button>
              </form>
            </Form>
          </CardContent>
        </Card>

        <div>
          {result ? (
            <EvaluationResultView result={result as any} />
          ) : (
            <Card className="h-full border-dashed flex items-center justify-center min-h-[400px] text-muted-foreground">
              Submit a response to see the evaluation.
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
