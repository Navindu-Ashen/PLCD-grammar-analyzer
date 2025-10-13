"use client";

import { useState, forwardRef } from "react";
import { Zap, Loader2, AlertTriangle } from "lucide-react";
import { ShineBorder } from "@/components/magicui/shine-border";

interface InputSectionProps {
  expression: string;
  setExpression: (value: string) => void;
  onAnalyze: () => void;
  loading: boolean;
  error: string;
  isVisible: boolean;
}

const InputSection = forwardRef<HTMLElement, InputSectionProps>(
  (
    { expression, setExpression, onAnalyze, loading, error, isVisible },
    ref,
  ) => {
    const exampleExpressions = [
      "int x = 5",
      "double y = 3.14",
      "x + y * 2",
      "if (x > 0)",
      "while (i < 10)",
      "bool flag = true",
      'string name = "hello"',
    ];

    const handleKeyPress = (e: React.KeyboardEvent) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        onAnalyze();
      }
    };

    const handleExampleClick = (example: string) => {
      setExpression(example);
    };

    return (
      <section className="py-4" ref={ref}>
        <div
          className={`relative bg-white/80 dark:bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 mb-8 border border-slate-200 dark:border-slate-700 shadow-lg fade-in fade-in-delay-2 ${isVisible ? "visible" : ""}`}
        >
          <ShineBorder shineColor={["#3B82F6", "#1E40AF", "#60A5FA"]} />

          <label
            htmlFor="expression"
            className="block text-slate-900 dark:text-white text-lg font-medium mb-3"
          >
            Enter Your Programming Expression
          </label>
          <p className="text-slate-600 dark:text-slate-400 text-sm mb-4">
            Type any programming language expression below and click "Analyze"
            for complete compilation analysis.
          </p>
          <div className="flex flex-col sm:flex-row gap-4">
            <input
              id="expression"
              type="text"
              value={expression}
              onChange={(e) => setExpression(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Try: int x = 5, float y = x * 2.5, if (x == 5), etc."
              className="flex-1 px-4 py-3 rounded-lg bg-slate-100 dark:bg-slate-700 text-slate-900 dark:text-white placeholder-slate-500 dark:placeholder-slate-400 border border-slate-300 dark:border-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
            />
            <button
              onClick={onAnalyze}
              disabled={loading}
              className="px-8 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors flex items-center justify-center gap-2 min-w-[140px]"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Analysing...
                </>
              ) : (
                <>
                  <Zap className="w-4 h-4" />
                  Analyse
                </>
              )}
            </button>
          </div>

          <div className="mt-4">
            <p className="text-slate-600 dark:text-slate-400 text-sm mb-3">
              Quick Examples - Click to try:
            </p>
            <div className="flex flex-wrap gap-2">
              {exampleExpressions.map((example, index) => (
                <button
                  key={index}
                  onClick={() => handleExampleClick(example)}
                  className="px-3 py-2 text-sm bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-300 rounded-lg transition-colors border border-slate-300 dark:border-slate-600 hover:border-slate-400 dark:hover:border-slate-500"
                >
                  <code>{example}</code>
                </button>
              ))}
            </div>
          </div>

          {error && (
            <div className="mt-4 p-3 bg-red-100 dark:bg-red-900/50 border border-red-300 dark:border-red-700 rounded-lg">
              <p className="text-red-700 dark:text-red-400 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 flex-shrink-0" />
                <span className="break-words">{error}</span>
              </p>
            </div>
          )}
        </div>
      </section>
    );
  },
);

InputSection.displayName = "InputSection";

export default InputSection;
