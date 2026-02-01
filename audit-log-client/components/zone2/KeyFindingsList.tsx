export const KeyFindingsList: React.FC<{ findings: string[] }> = ({
  findings,
}) => {
  if (!findings.length) return null;

  return (
    <div>
      <h4 className="text-xs uppercase tracking-widest text-brand-cream/40 mb-6">
        Key Findings
      </h4>

      <ul className="space-y-4">
        {findings.map((f, i) => (
          <li
            key={i}
            className="flex gap-3 text-brand-cream/80 text-base"
          >
            <span>•</span>
            <span>{f}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};
