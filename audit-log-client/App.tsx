import React, { useState, useEffect } from 'react';
import { AuditForm } from './components/AuditForm';
import { AuditResult } from './components/AuditResult';
import { ErrorDisplay } from './components/ErrorDisplay';
import { submitAuditRequest } from './services/auditService';
import { Audience, AuditResponse, ApiErrorDetail } from './types';

type ViewState = 'idle' | 'loading' | 'success' | 'error';

// Reactive Reticle Logo
const Logo = () => (
  <div className="relative w-10 h-10 flex items-center justify-center mr-3">
    {/* Outer Scanning Ring */}
    <div className="absolute inset-0 rounded-full border border-brand-cream/20 border-dashed animate-[spin_10s_linear_infinite] group-hover:animate-[spin_4s_linear_infinite] group-hover:border-brand-red/50 transition-colors duration-500"></div>
    
    {/* Targeting Brackets */}
    <div className="absolute inset-1 border-x border-brand-cream/60 rounded-sm scale-90 group-hover:scale-100 group-hover:border-brand-red group-hover:rotate-180 transition-all duration-500 ease-[cubic-bezier(0.25,1,0.5,1)]"></div>
    
    {/* Core Status Light */}
    <div className="w-2 h-2 bg-brand-cream rounded-full group-hover:bg-brand-red shadow-[0_0_10px_rgba(255,255,255,0.5)] group-hover:shadow-[0_0_15px_rgba(255,59,48,0.8)] transition-all duration-300"></div>
  </div>
);

const LOADING_LOGS = [
  "Initializing secure handshake...",
  "Validating CSV schema structure...",
  "Parsing headers and delimiters...",
  "Analyzing entropy levels...",
  "Checking for deterministic anomalies...",
  "Formatting audit vectors...",
  "Compiling executive summary...",
  "Finalizing decision engine..."
];

export default function App() {
  const [viewState, setViewState] = useState<ViewState>('idle');
  const [result, setResult] = useState<AuditResponse | null>(null);
  const [error, setError] = useState<ApiErrorDetail | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [logIndex, setLogIndex] = useState(0);
  
  const [lastSubmission, setLastSubmission] = useState<{
    dataset: File;
    audience: Audience;
    metadata?: File;
  } | null>(null);

  // Cycle through logs during loading
  useEffect(() => {
    if (viewState === 'loading') {
      const interval = setInterval(() => {
        setLogIndex(prev => (prev + 1) % LOADING_LOGS.length);
      }, 800);
      return () => clearInterval(interval);
    } else {
      setLogIndex(0);
    }
  }, [viewState]);

  const handleAuditSubmit = async (dataset: File, audience: Audience, metadata?: File) => {
    setViewState('loading');
    setUploadProgress(0);
    setLastSubmission({ dataset, audience, metadata });
    setError(null);

    try {
      const data = await submitAuditRequest(
        dataset, 
        audience, 
        metadata, 
        (percent) => setUploadProgress(percent)
      );
      setResult(data);
      setViewState('success');
    } catch (err) {
      const apiError = err as ApiErrorDetail;
      setError(apiError);
      setViewState('error');
    }
  };

  const handleRetry = () => {
    if (lastSubmission) {
      handleAuditSubmit(lastSubmission.dataset, lastSubmission.audience, lastSubmission.metadata);
    }
  };

  const handleReset = () => {
    setViewState('idle');
    setResult(null);
    setError(null);
    setLastSubmission(null);
    setUploadProgress(0);
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background Texture - Dark Noise */}
      <div className="fixed inset-0 bg-noise opacity-20 pointer-events-none z-0 mix-blend-overlay"></div>
      
      {/* Marquee Header - Dark Mode Style */}
      <div className="relative z-10 w-full border-b border-white/10 py-3 bg-brand-black/50 backdrop-blur-sm">
        <div className="animate-marquee whitespace-nowrap flex gap-12 text-[10px] font-mono tracking-[0.2em] uppercase items-center text-brand-cream/40">
          <span>// Audit Engine v1.0</span>
          <span>// Secure Environment</span>
          <span>// Deterministic Analysis</span>
          <span>// ISO 27001 Compliant</span>
          <span>// Audit Engine v1.0</span>
          <span>// Secure Environment</span>
          <span>// Deterministic Analysis</span>
          <span>// ISO 27001 Compliant</span>
          <span>// Audit Engine v1.0</span>
          <span>// Secure Environment</span>
        </div>
      </div>

      <div className="relative z-10 max-w-5xl mx-auto px-6 py-12 md:py-24">
        
        {/* Navigation */}
        <header className="flex items-center justify-between mb-24 animate-fade-in">
          <div className="flex items-center group cursor-pointer pl-1" onClick={handleReset}>
            <Logo />
            <span className="font-serif text-2xl font-bold text-brand-cream tracking-tight group-hover:text-brand-red transition-colors duration-300">AuditEngine.</span>
          </div>
          <div className="flex items-center gap-2 text-xs font-mono text-brand-cream/60 border border-white/10 px-4 py-1.5 rounded-full backdrop-blur-md">
            <div className={`w-1.5 h-1.5 rounded-full ${viewState === 'loading' ? 'bg-brand-red animate-pulse' : 'bg-brand-lime'}`}></div>
            SYSTEM {viewState === 'loading' ? 'BUSY' : 'READY'}
          </div>
        </header>

        <main>
          {viewState === 'idle' && (
            <div className="animate-slide-up">
              <div className="mb-20 grid grid-cols-1 md:grid-cols-12 gap-8 items-end">
                <div className="md:col-span-8">
                   <h1 className="text-5xl md:text-7xl font-serif text-brand-cream leading-[0.95] tracking-tight mb-8 group/headline cursor-default select-none">
                     
                     {/* Line 1 */}
                     <span className="block overflow-hidden pb-2 -mb-2">
                       <span className="block animate-reveal-up" style={{ animationDelay: '0ms' }}>
                          <span className="block transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)] opacity-60 blur-[0.5px] group-hover/headline:opacity-100 group-hover/headline:blur-0 group-hover/headline:translate-x-2">
                            Making system risks
                          </span>
                       </span>
                     </span>
                     
                     {/* Line 2 */}
                     <span className="block overflow-hidden pb-2 -mb-2">
                       <span className="block animate-reveal-up" style={{ animationDelay: '150ms' }}>
                          <span className="block transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)] group-hover/headline:translate-x-3">
                             {/* Stable 'explicit' - Color and glow only, no width change */}
                            <span className="italic text-brand-cream/60 transition-all duration-500 group-hover/headline:text-brand-red group-hover/headline:drop-shadow-[0_0_12px_rgba(255,59,48,0.5)]">explicit</span>
                            <span className="opacity-60 blur-[0.5px] transition-all duration-700 group-hover/headline:opacity-100 group-hover/headline:blur-0 group-hover/headline:text-white ml-3">before they</span>
                          </span>
                       </span>
                     </span>

                     {/* Line 3 */}
                     <span className="block overflow-hidden pb-2 -mb-2">
                       <span className="block animate-reveal-up" style={{ animationDelay: '300ms' }}>
                          <span className="block transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)] opacity-60 blur-[0.5px] group-hover/headline:opacity-100 group-hover/headline:blur-0 group-hover/headline:translate-x-4">
                            become failures.
                          </span>
                       </span>
                     </span>
                  </h1>
                </div>
                <div className="md:col-span-4 pb-2">
                   <p className="text-lg text-brand-cream/60 leading-relaxed max-w-xs ml-auto animate-fade-in" style={{ animationDelay: '600ms' }}>
                    Upload raw datasets to generate auditor-grade compliance reports with deterministic precision.
                  </p>
                </div>
              </div>
              <div className="animate-fade-in" style={{ animationDelay: '800ms' }}>
                <AuditForm 
                  onSubmit={handleAuditSubmit} 
                  isLoading={false} 
                  uploadProgress={0}
                />
              </div>
            </div>
          )}

          {viewState === 'loading' && (
            <div className="animate-fade-in flex flex-col items-center justify-center min-h-[40vh]">
               <div className="mb-12 pointer-events-none opacity-10 blur-sm absolute top-40 inset-x-0 text-center">
                 <h1 className="text-6xl md:text-8xl font-serif text-white leading-[0.9]">
                  Verifying<br/> 
                  Integrity.
                </h1>
              </div>
              
              <div className="relative z-10 w-full max-w-md bg-[#111] p-1 rounded-3xl border border-white/10 shadow-2xl shadow-brand-red/5">
                 <div className="bg-brand-black rounded-[20px] p-8 border border-white/5">
                    <div className="w-16 h-16 border-2 border-brand-gray border-t-brand-red rounded-full animate-spin-slow mx-auto mb-6"></div>
                    <h3 className="text-2xl font-serif text-brand-cream mb-2 text-center">Processing Data</h3>
                    
                    {/* Dynamic System Logs */}
                    <div className="h-6 mb-8 overflow-hidden relative">
                        {LOADING_LOGS.map((log, i) => (
                           <p 
                            key={i} 
                            className={`
                                absolute w-full text-center text-sm font-mono transition-all duration-500
                                ${i === logIndex ? 'opacity-100 transform translate-y-0 text-brand-cream/60' : 'opacity-0 transform translate-y-4 text-brand-cream/20'}
                            `}
                           >
                            {">"} {log}
                           </p>
                        ))}
                    </div>
                    
                    <div className="w-full bg-brand-gray h-1 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-brand-red transition-all duration-300 ease-out"
                          style={{ width: `${Math.max(5, uploadProgress)}%` }}
                        ></div>
                    </div>
                    <div className="flex justify-between text-[10px] font-mono text-brand-cream/40 mt-3">
                        <span>UPLOAD SEQUENCE</span>
                        <span>{Math.round(uploadProgress)}%</span>
                    </div>
                 </div>
              </div>
            </div>
          )}

          {viewState === 'success' && result && (
            <AuditResult data={result} onReset={handleReset} />
          )}

          {viewState === 'error' && error && (
            <div className="space-y-8 animate-slide-up">
              <ErrorDisplay 
                error={error} 
                onRetry={handleRetry} 
                onReset={handleReset} 
              />
            </div>
          )}
        </main>
      </div>
    </div>
  );
}