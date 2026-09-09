export interface Scenario {
  id: string;
  name: string;
  industry: string;
  stage: string;
  count: number;
  description?: string;
  prospectProfile?: string;
  objection: string;
  hiddenConcerns?: string[];
  evaluationCriteria?: string[];
}

export type CreateScenarioInput = Omit<Scenario, "id" | "count">;
export type UpdateScenarioInput = Partial<CreateScenarioInput>;
