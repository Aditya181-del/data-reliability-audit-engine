export const SummaryCard: React.FC<{ text: string }> = ({ text }) => {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-10">
      <h4 className="text-sm uppercase tracking-widest text-brand-cream/40 mb-4">
        Why this decision was reached
      </h4>
      <p className="text-2xl font-serif text-brand-cream leading-relaxed">
        {text}
      </p>
    </div>
  );
};
