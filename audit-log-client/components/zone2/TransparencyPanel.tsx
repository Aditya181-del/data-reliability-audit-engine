import { useState } from 'react';

export const TransparencyPanel: React.FC<{ audit: unknown }> = ({
  audit,
}) => {
  const [open, setOpen] = useState(false);

  return (
    <div>
      <button
        onClick={() => setOpen(!open)}
        className="text-xs font-mono text-brand-cream/40 hover:text-brand-cream"
      >
        {open ? 'Hide raw audit evidence' : 'View raw audit evidence'}
      </button>

      {open && (
        <pre className="mt-4 bg-[#050505] p-6 rounded-2xl text-xs overflow-auto">
          {JSON.stringify(audit, null, 2)}
        </pre>
      )}
    </div>
  );
};
