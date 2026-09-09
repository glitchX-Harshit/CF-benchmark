"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Plus, Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import Link from "next/link";

export default function ScenariosPage() {
  const scenarios = [
    { id: "1", name: "Budget Too Small", industry: "SaaS", stage: "Discovery", count: 45 },
    { id: "2", name: "Using Competitor X", industry: "Any", stage: "Qualification", count: 112 },
    { id: "3", name: "Need to consult boss", industry: "Manufacturing", stage: "Closing", count: 34 },
    { id: "4", name: "Missing critical feature", industry: "SaaS", stage: "Demo", count: 67 },
    { id: "5", name: "Not a priority right now", industry: "Any", stage: "Discovery", count: 89 },
    { id: "6", name: "Too difficult to implement", industry: "Enterprise", stage: "Proposal", count: 21 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Scenarios</h1>
          <p className="text-muted-foreground">Manage and evaluate against standardized sales scenarios.</p>
        </div>
        <Button asChild>
          <Link href="/scenarios/new">
            <Plus className="mr-2 h-4 w-4" /> New Scenario
          </Link>
        </Button>
      </div>

      <div className="flex items-center space-x-2">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input type="search" placeholder="Search scenarios..." className="pl-8" />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {scenarios.map(s => (
          <Card key={s.id} className="hover:border-blue-500 transition-colors cursor-pointer group">
            <Link href={`/scenarios/${s.id}`}>
              <CardHeader className="pb-3">
                <CardTitle className="text-lg group-hover:text-blue-600 transition-colors">{s.name}</CardTitle>
                <CardDescription>Evaluated {s.count} times</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex gap-2">
                  <Badge variant="outline">{s.industry}</Badge>
                  <Badge variant="secondary">{s.stage}</Badge>
                </div>
              </CardContent>
            </Link>
          </Card>
        ))}
      </div>
    </div>
  );
}
