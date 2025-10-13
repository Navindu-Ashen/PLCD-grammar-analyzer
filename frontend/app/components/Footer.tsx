"use client";

interface FooterProps {
  isVisible: boolean;
}

export default function Footer({ isVisible }: FooterProps) {
  return (
    <div
      className={`max-w-6xl mx-auto mt-12 fade-in fade-in-delay-4 ${isVisible ? "visible" : ""}`}
    >
      <div className="text-center py-6 border-t border-slate-300 dark:border-slate-700">
        <p className="text-slate-600 dark:text-slate-400 text-sm">
          Programming Language Compiler Design Final Project - Group V
          <br />
          Built with Next.js, TypeScript, and Python
        </p>
      </div>
    </div>
  );
}
