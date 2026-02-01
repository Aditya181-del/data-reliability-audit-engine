import React, { useRef, useState } from 'react';

interface FileInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  helperText?: string;
  onFileSelect: (file: File | null) => void;
  selectedFileName?: string | null;
  progress?: number;
}

export const FileInput: React.FC<FileInputProps> = ({ 
  label, 
  helperText, 
  onFileSelect, 
  selectedFileName, 
  id,
  required,
  progress,
  disabled,
  ...props 
}) => {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files && e.target.files.length > 0 ? e.target.files[0] : null;
    onFileSelect(file);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    if (!disabled) setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (disabled) return;

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      // trigger the select
      onFileSelect(file);
      // Manually update the input ref so the change event logic stays consistent if needed elsewhere
      if (inputRef.current) {
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        inputRef.current.files = dataTransfer.files;
      }
    }
  };

  const hasFile = !!selectedFileName;
  const isUploading = typeof progress === 'number' && progress >= 0 && progress < 100;

  return (
    <div className="group">
      <label htmlFor={id} className="block text-xs font-bold uppercase tracking-widest text-brand-cream/60 mb-3 transition-colors group-hover:text-brand-cream">
        {label} {required && <span className="text-brand-red">*</span>}
      </label>
      
      <div 
        onClick={() => !disabled && inputRef.current?.click()}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`
          relative flex items-center justify-between p-5 border rounded-2xl overflow-hidden backdrop-blur-sm
          transform transition-all duration-300 ease-out
          focus-within:outline-none focus-within:ring-1 focus-within:ring-brand-red focus-within:border-brand-red
          ${disabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer hover:shadow-2xl hover:shadow-brand-lime/10'}
          ${isDragging 
            ? 'scale-[1.03] border-brand-lime bg-brand-lime/10 shadow-xl shadow-brand-lime/20' 
            : 'hover:scale-[1.02] hover:-translate-y-1'
          }
          ${hasFile 
            ? 'border-brand-lime/50 bg-brand-lime/10 shadow-lg shadow-brand-lime/5' 
            : isDragging ? '' : 'border-white/10 bg-white/5 hover:border-white/30 hover:bg-white/10'
          }
        `}
      >
        {/* Progress Bar Background */}
        {isUploading && (
          <div 
            className="absolute bottom-0 left-0 h-1 bg-brand-lime transition-all duration-300 ease-out"
            style={{ width: `${progress}%` }}
          />
        )}

        <input
          ref={inputRef}
          type="file"
          id={id}
          className="sr-only"
          onChange={handleChange}
          disabled={disabled}
          {...props}
        />
        
        <div className="flex items-center gap-5 overflow-hidden z-10 w-full pointer-events-none">
          {/* Circle Icon */}
          <div className={`
            w-12 h-12 min-w-[3rem] min-h-[3rem] aspect-square rounded-full flex items-center justify-center flex-shrink-0 
            transition-[transform,background-color,color] duration-500 ease-[cubic-bezier(0.25,1,0.5,1)] transform-gpu
            ${hasFile || isDragging ? 'bg-brand-lime text-brand-black rotate-[-10deg]' : 'bg-white/10 text-brand-cream/40 group-hover:bg-brand-cream group-hover:text-brand-black'}
          `}>
            {isUploading ? (
              <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : hasFile ? (
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            ) : (
              <svg className={`w-5 h-5 transition-transform duration-500 ease-[cubic-bezier(0.25,1,0.5,1)] ${isDragging ? 'scale-125' : 'group-hover:scale-125'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
            )}
          </div>
          
          <div className="flex flex-col min-w-0 flex-grow">
            <span className={`text-sm font-sans font-medium truncate transition-colors duration-300 ${hasFile || isDragging ? 'text-brand-lime' : 'text-brand-cream/80 group-hover:text-brand-cream'}`}>
              {isUploading 
                ? `Uploading... ${Math.round(progress!)}%` 
                : isDragging 
                  ? "Drop to attach" 
                  : (selectedFileName || "Select or drop file")}
            </span>
            {(!hasFile && !isDragging) && helperText && (
              <span className="text-xs text-brand-cream/30 truncate hidden sm:block font-mono tracking-tight mt-1 transition-colors duration-300 group-hover:text-brand-cream/50">
                {helperText}
              </span>
            )}
          </div>
        </div>

        {hasFile && !disabled && (
          <button 
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onFileSelect(null);
              if(inputRef.current) inputRef.current.value = '';
            }}
            className="p-2 -mr-2 hover:bg-white/10 rounded-full text-brand-cream/40 hover:text-brand-red transition-colors z-10 group/clear"
          >
             <svg className="w-5 h-5 transition-transform group-hover/clear:rotate-90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
          </button>
        )}
      </div>
    </div>
  );
};