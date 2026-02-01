export type Audience =
  | 'engineer'
  | 'product'
  | 'executive'
  | 'compliance';

export interface Zone2Explanation {
  audience: Audience;

  summary: string;

  key_findings: string[];

  decision_rationale: string;

  next_steps: string[];

  disclaimer?: string;
}
