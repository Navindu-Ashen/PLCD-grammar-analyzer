"use client";

import { Brain } from "lucide-react";

interface AnalysisProcessProps {
  isVisible: boolean;
}

export default function AnalysisProcess({ isVisible }: AnalysisProcessProps) {
  return (
    <div
      className={`bg-white/60 dark:bg-slate-800/30 backdrop-blur-sm rounded-xl p-6 border border-slate-200 dark:border-slate-700 shadow-lg fade-in fade-in-delay-3 ${isVisible ? "visible" : ""}`}
    >
      <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-6 flex items-center gap-2">
        <Brain className="w-5 h-5 text-blue-500 dark:text-blue-400" />
        Analysis Process
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-100 dark:bg-slate-800/50 rounded-lg p-4 border border-slate-200 dark:border-slate-700">
          <h4 className="text-blue-600 dark:text-blue-400 font-medium mb-2">
            1. Lexical Analysis
          </h4>
          <p className="text-slate-700 dark:text-slate-400 text-sm">
            Breaks down your expression into tokens (keywords,
            identifiers, operators, literals)
          </p>
        </div>
        <div className="bg-slate-100 dark:bg-slate-800/50 rounded-lg p-4 border border-slate-200 dark:border-slate-700">
          <h4 className="text-blue-600 dark:text-blue-400 font-medium mb-2">
            2. Syntax Analysis
          </h4>
          <p className="text-slate-700 dark:text-slate-400 text-sm">
            Validates grammar rules and structural correctness of your
            expression
          </p>
        </div>
        <div className="bg-slate-100 dark:bg-slate-800/50 rounded-lg p-4 border border-slate-200 dark:border-slate-700">
          <h4 className="text-blue-600 dark:text-blue-400 font-medium mb-2">
            3. Semantic Analysis
          </h4>
          <p className="text-slate-700 dark:text-slate-400 text-sm">
            Checks types, variable declarations, and logical consistency
          </p>
        </div>
      </div>
      <div className="mt-6 p-4 bg-blue-100 dark:bg-blue-900/20 border border-blue-300 dark:border-blue-700 rounded-lg">
        <p className="text-blue-700 dark:text-blue-300 text-sm">
          💡 <strong>Tip:</strong> Start with simple expressions like
          "int x = 5" to understand the analysis process, then try more
          complex expressions!
        </p>
      </div>
    </div>
  );
}
