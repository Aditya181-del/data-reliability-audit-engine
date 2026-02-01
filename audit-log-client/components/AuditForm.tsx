import React, { useState } from 'react';
import { Audience, AUDIENCE_OPTIONS } from '../types';
import { Button } from './ui/Button';
import { FileInput } from './ui/FileInput';

interface AuditFormProps {
  onSubmit: (dataset: File, audience: Audience, metadata?: File) => void;
  isLoading: boolean;
  uploadProgress: number; 
}

export const AuditForm: React.FC<AuditFormProps> = ({ onSubmit, isLoading, uploadProgress }) => {
  const [dataset, setDataset] = useState<File | null>(null);
  const [metadata, setMetadata] = useState<File | null>(null);
  const [audience, setAudience] = useState<Audience>('engineer');
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (dataset) {
      onSubmit(dataset, audience, metadata || undefined);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="animate-slide-up">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        <div className="md:col-span-2">
          <FileInput
            id="dataset-upload"
            label="Dataset (CSV)"
            accept=".csv"
            required
            onFileSelect={setDataset}
            selectedFileName={dataset?.name}
            helperText="Raw system logs or transaction data."
            disabled={isLoading}
            progress={isLoading ? uploadProgress : undefined}
          />
        </div>

      
        <FileInput
          id="metadata-upload"
          label="Metadata (YAML) *Required"
          accept=".yaml,.yml"
          required
          onFileSelect={setMetadata}
          selectedFileName={metadata?.name}
          helperText="Target column and audit context configuration."
          disabled={isLoading}
        />


        <div>
          <label htmlFor="audience-select" className="block text-xs font-bold uppercase tracking-widest text-brand-cream/60 mb-3">
            Target Audience
          </label>
          <div className="relative group">
            <select
              id="audience-select"
              value={audience}
              onChange={(e) => setAudience(e.target.value as Audience)}
              disabled={isLoading}
              className="block w-full h-[88px] pl-6 pr-10 py-4 text-base font-medium text-brand-cream border border-white/10 rounded-2xl focus:outline-none focus:border-brand-red focus:ring-1 focus:ring-brand-red focus:bg-white/5 sm:text-sm appearance-none bg-white/5 hover:bg-white/10 hover:border-white/30 transition-all cursor-pointer"
            >
              {AUDIENCE_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value} className="bg-brand-black text-brand-cream py-2">
                  {opt.label}
                </option>
              ))}
            </select>
            <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-6 text-brand-cream/40 group-hover:text-brand-cream transition-colors">
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-between gap-6 pt-8 border-t border-white/10">
        <p className="text-sm text-brand-cream/40 font-mono">
          * Analysis is deterministic and runs locally.
        </p>
        <Button 
          type="submit" 
          disabled={!dataset} 
          isLoading={isLoading}
          className="w-full sm:w-auto min-w-[200px]"
        >
          {isLoading && uploadProgress < 100 ? `Uploading ${Math.round(uploadProgress)}%` : 'Run Analysis'}
        </Button>
      </div>
    </form>
  );
};