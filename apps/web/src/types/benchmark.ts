export interface Benchmark {
  id: string;
  name: string;
  description: string;
  averageScore: number;
  percentile75: number;
  percentile90: number;
  industry: string;
  dataPoints: number;
  lastUpdated: string;
}
