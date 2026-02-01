export const NextSteps: React.FC<{ steps: string[] }> = ({ steps }) => {
  if (!steps.length) return null;

  return (
    <div>
      <h4 className="text-xs uppercase tracking-widest text-brand-cream/40 mb-6">
        What should be addressed next
      </h4>

      <ul className="space-y-3">
        {steps.map((s, i) => (
          <li key={i} className="text-brand-cream/70">
            • {s}
          </li>
        ))}
      </ul>
    </div>
  );
};
