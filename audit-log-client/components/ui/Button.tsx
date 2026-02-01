import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'outline';
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ 
  children, 
  variant = 'primary', 
  isLoading, 
  disabled, 
  className = '', 
  ...props 
}) => {
  const baseStyles = "relative overflow-hidden inline-flex items-center justify-center px-8 py-4 text-sm font-bold tracking-wider uppercase transition-all duration-300 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed group active:scale-95";
  
  const variants = {
    // Brand Red - The "Let's Connect" style
    primary: "bg-brand-red text-white hover:bg-[#ff5540] rounded-full shadow-[0_0_20px_-5px_rgba(255,59,48,0.4)] hover:shadow-[0_0_30px_-5px_rgba(255,59,48,0.6)]",
    // Dark Gray surface
    secondary: "bg-brand-gray text-brand-cream hover:bg-white/10 rounded-full",
    // Error state
    danger: "bg-red-900/50 text-red-200 border border-red-800 hover:bg-red-900 hover:text-white rounded-full",
    // White outline
    outline: "border border-brand-cream/30 text-brand-cream hover:border-brand-cream hover:bg-brand-cream hover:text-brand-black bg-transparent rounded-full"
  };

  return (
    <button 
      disabled={disabled || isLoading}
      className={`${baseStyles} ${variants[variant]} ${className}`}
      {...props}
    >
      {isLoading ? (
        <span className="flex items-center justify-center gap-2 relative z-10">
          <svg className="animate-spin h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Processing
        </span>
      ) : (
        <span className="relative z-10 flex items-center gap-2 group-hover:-translate-y-0.5 transition-transform duration-300 font-sans">
            {children}
        </span>
      )}
    </button>
  );
};