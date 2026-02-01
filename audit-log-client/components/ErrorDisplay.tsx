import React from 'react';
import { ApiErrorDetail } from '../types';
import { Button } from './ui/Button';

interface ErrorDisplayProps {
  error: ApiErrorDetail;
  onRetry: () => void;
  onReset: () => void;
}

export const ErrorDisplay: React.FC<ErrorDisplayProps> = ({ error, onRetry, onReset }) => {
  const isRetryable = error.type === 'network' || error.status === 500 || error.status === 503;

  return (
    <div className="bg-red-950/30 border border-red-900/50 rounded-2xl p-8 shadow-lg shadow-red-900/10 backdrop-blur-sm" role="alert">
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <svg className="h-6 w-6 text-brand-red" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <div className="ml-5 flex-grow">
          <h3 className="text-lg font-serif font-medium text-red-100">
            Audit Request Failed
          </h3>
          <div className="mt-2 text-red-200/80">
            <p className="font-medium">{error.message}</p>
          </div>
          
          {error.rawResponse && (
            <div className="mt-6">
               <span className="text-[10px] font-bold text-red-300 uppercase tracking-widest">Raw Server Response (Debug):</span>
               <div className="mt-2 p-4 bg-black/50 rounded-xl text-xs font-mono text-red-200 overflow-x-auto whitespace-pre-wrap max-h-40 border border-red-900/30">
                 {error.rawResponse.slice(0, 500)}
                 {error.rawResponse.length > 500 && '... (truncated)'}
               </div>
            </div>
          )}

          <div className="mt-8 flex gap-4">
            {isRetryable && (
              <Button onClick={onRetry} variant="danger" className="text-sm px-6">
                Retry Request
              </Button>
            )}
            <Button onClick={onReset} variant="outline" className="text-sm px-6 border-red-900/50 text-red-200 hover:bg-red-900/20 hover:border-red-800">
              Clear & Start Over
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};