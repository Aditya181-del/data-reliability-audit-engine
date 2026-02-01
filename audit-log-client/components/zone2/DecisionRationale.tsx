export const DecisionRationale: React.FC<{ text: string }> = ({ text }) => {
  return (
    <div className="rounded-2xl border border-white/10 p-8 bg-black/20">
      <h4 className="text-xs uppercase tracking-widest text-brand-cream/40 mb-4">
        Why action is required
      </h4>
      <p className="text-brand-cream/80 leading-relaxed">
        {text}
      </p>
    </div>
  );
};
