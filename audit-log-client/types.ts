// frontend/src/types.ts

export type Audience = 'engineer' | 'executive' | 'auditor';

export const AUDIENCE_OPTIONS: Array<{
  value: Audience;
  label: string;
}> = [
  { value: 'engineer', label: 'Engineer / ML Practitioner' },
  { value: 'executive', label: 'Executive / Decision Maker' },
  { value: 'auditor', label: 'Auditor / Compliance' },
];

// --------------------
// Audit API responses
// --------------------

export type Decision = 'PROCEED' | 'FIX' | 'ABORT';

export interface Explanation {
  summary: string;
  key_insights?: string[];
  limitations?: string;
  disclaimer?: string;
}

export interface AuditResponse {
  decision: Decision | string;
  audit: Record<string, any>;
  explanation?: Explanation | null;
}


