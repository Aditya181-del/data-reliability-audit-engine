import { Audience } from './types';

interface Props {
  value: Audience;
  onChange: (a: Audience) => void;
}

export const AudienceSelector: React.FC<Props> = ({ value, onChange }) => {
  return (
    <div className="flex items-center justify-between">
      <h3 className="text-xs uppercase tracking-widest text-brand-cream/40">
        Explanation (Non-authoritative)
      </h3>

      <select
        value={value}
        onChange={(e) => onChange(e.target.value as Audience)}
        className="bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-sm"
      >
        <option value="engineer">Engineer</option>
        <option value="product">Product</option>
        <option value="executive">Executive</option>
        <option value="compliance">Compliance</option>
      </select>
    </div>
  );
};
