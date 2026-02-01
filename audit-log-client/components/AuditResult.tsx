// src/components/AuditResult.tsx

import React from 'react';
import { AuditResponse } from '../types';
import { Button } from './ui/Button';

interface Props {
  data: AuditResponse;
  onReset: () => void;
}

export const AuditResult: React.FC<Props> = ({ data, onReset }) => {
  const e = data.explanation;

  // ---------- Decision confidence (frontend-only heuristic) ----------
  const confidence =
    data.unassessed_risks?.length > 0
      ? 'Low'
      : data.summary?.high_severity_risks > 0
      ? 'Medium'
      : 'High';

  const confidenceColor =
    confidence === 'Low'
      ? 'text-red-400'
      : confidence === 'Medium'
      ? 'text-amber-400'
      : 'text-green-400';

  return (
    <div className="space-y-16 pb-24">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-serif text-brand-cream">
          Report Generated
        </h2>
        <Button onClick={onReset}>New Scan</Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-16">
        {/* =========================
            Zone 2 — Explanation
           ========================= */}
        <section className="lg:col-span-7 space-y-10 max-w-2xl">
          <h3 className="text-xs uppercase tracking-widest text-brand-cream/40">
            Explanation (Non-authoritative)
          </h3>

          {/* Headline */}
          <h2 className="text-3xl font-serif text-brand-cream">
            {e?.headline ?? 'Audit explanation'}
          </h2>

          {/* Summary */}
          <div className="space-y-6 text-brand-cream/80 text-lg leading-relaxed">
            {e?.summary
              ?.split('\n')
              .filter(Boolean)
              .map((para, i) => (
                <p key={i}>{para}</p>
              ))}
          </div>

          {/* Structural Risks */}
          {data.structural_risks?.length > 0 && (
            <div>
              <h4 className="text-sm uppercase tracking-widest text-brand-cream/40">
                Detected high-risk issues
              </h4>
              <ul className="mt-3 space-y-3">
                {data.structural_risks.map((risk, i) => (
                  <li
                    key={i}
                    className="text-brand-cream/80 flex items-start gap-3"
                  >
                    <span className="mt-1 h-2 w-2 rounded-full bg-red-400" />
                    <span>
                      <strong>{risk.risk_id}</strong> —{' '}
                      {risk.affected_columns.join(', ')}{' '}
                      <span className="text-xs text-brand-cream/50">
                        ({risk.severity} severity, {risk.confidence} confidence)
                      </span>
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Unassessed Risks */}
          {data.unassessed_risks?.length > 0 && (
            <div>
              <h4 className="text-sm uppercase tracking-widest text-brand-cream/40">
                Unassessed uncertainty
              </h4>
              <ul className="mt-3 space-y-2">
                {data.unassessed_risks.map((risk, i) => (
                  <li key={i} className="text-brand-cream/70">
                    • {risk.category.replace('_', ' ')}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Decision confidence */}
          <div className="pt-4 border-t border-white/10">
            <p className="text-sm text-brand-cream/60">
              Decision confidence:{' '}
              <span className={`font-semibold ${confidenceColor}`}>
                {confidence}
              </span>
            </p>
          </div>

          {/* Disclaimer */}
          <p className="text-xs text-brand-cream/40 font-mono">
            {e?.disclaimer}
          </p>
        </section>

        {/* =========================
            Right Panel — Raw Audit
           ========================= */}
        <section className="lg:col-span-5 bg-[#050505] p-6 rounded-3xl text-xs font-mono overflow-auto">
          <div className="text-brand-cream/40 mb-3">
            Audit Evidence (Machine-readable)
          </div>
          <pre>{JSON.stringify(data.audit, null, 2)}</pre>
        </section>
      </div>
    </div>
  );
};
