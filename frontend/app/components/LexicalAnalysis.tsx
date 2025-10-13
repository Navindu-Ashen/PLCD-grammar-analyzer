"use client";

import { Code } from "lucide-react";
import { AnalysisResponse } from "../types/analysis";

interface LexicalAnalysisProps {
  result: AnalysisResponse;
}

export default function LexicalAnalysis({ result }: LexicalAnalysisProps) {
  return (
    <div className="bg-white/80 dark:bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-200 dark:border-slate-700 shadow-lg">
      <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
        <Code className="w-5 h-5 text-blue-500 dark:text-blue-400" />
        Lexical Analysis
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="border-b border-slate-300 dark:border-slate-600">
              <th className="text-left py-3 px-4 text-slate-900 dark:text-white font-medium">
                Token Type
              </th>
              <th className="text-left py-3 px-4 text-slate-900 dark:text-white font-medium">
                Lexeme
              </th>
              <th className="text-left py-3 px-4 text-slate-900 dark:text-white font-medium">
                Category
              </th>
            </tr>
          </thead>
          <tbody>
            {result.lexical_analysis.tokens.map((token, index) => (
              <tr
                key={index}
                className="border-b border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/30"
              >
                <td className="py-3 px-4 text-slate-700 dark:text-slate-300 font-mono text-sm">
                  {token.token_type}
                </td>
                <td className="py-3 px-4 text-slate-900 dark:text-white font-mono">
                  {token.lexeme}
                </td>
                <td className="py-3 px-4">
                  <span className="px-2 py-1 bg-blue-200 dark:bg-blue-600/20 text-blue-800 dark:text-blue-300 rounded text-sm font-medium">
                    {token.category}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
