"use client";

import { Code, CheckCircle, XCircle, AlertTriangle } from "lucide-react";
import { AnalysisResponse } from "../types/analysis";

interface SyntaxAnalysisProps {
  result: AnalysisResponse;
}

export default function SyntaxAnalysis({ result }: SyntaxAnalysisProps) {
  return (
    <div className="bg-white/80 dark:bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-200 dark:border-slate-700 shadow-lg">
      <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
        <Code className="w-5 h-5 text-blue-500 dark:text-blue-400" />
        Syntax Analysis
      </h3>

      <div className="mb-4">
        <div
          className={`flex items-center gap-2 p-4 rounded-lg border ${
            result.syntax_analysis.accepted
              ? "bg-green-100 dark:bg-green-900/20 border-green-300 dark:border-green-700"
              : "bg-red-100 dark:bg-red-900/20 border-red-300 dark:border-red-700"
          }`}
        >
          {result.syntax_analysis.accepted ? (
            <>
              <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0" />
              <span className="text-green-400 font-medium">
                Syntax is valid
              </span>
            </>
          ) : (
            <>
              <XCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
              <span className="text-red-400 font-medium">
                Syntax errors detected
              </span>
            </>
          )}
        </div>
      </div>

      {result.syntax_analysis.errors &&
      result.syntax_analysis.errors.length > 0 ? (
        <div>
          <h4 className="text-lg font-medium text-slate-900 dark:text-white mb-3">
            Syntax Errors
          </h4>
          <div className="space-y-2">
            {result.syntax_analysis.errors.map((error, index) => (
              <div
                key={index}
                className="bg-red-100 dark:bg-red-900/20 border border-red-300 dark:border-red-700 rounded-lg p-3"
              >
                <p className="text-red-700 dark:text-red-400 flex items-start gap-2">
                  <XCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                  <span className="break-words">{error}</span>
                </p>
              </div>
            ))}
          </div>
        </div>
      ) : result.syntax_analysis.accepted ? (
        <div className="bg-green-100 dark:bg-green-900/20 border border-green-300 dark:border-green-700 rounded-lg p-4">
          <p className="text-green-700 dark:text-green-400 flex items-center gap-2">
            <CheckCircle className="w-4 h-4 flex-shrink-0" />
            No syntax errors found
          </p>
        </div>
      ) : (
        <div className="bg-slate-100 dark:bg-slate-700/50 border border-slate-300 dark:border-slate-600 rounded-lg p-4">
          <p className="text-slate-700 dark:text-slate-400 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 flex-shrink-0" />
            Syntax analysis failed - check your expression
          </p>
        </div>
      )}

      {/* BNF Derivation */}
      {result.syntax_analysis.bnf_derivation &&
        result.syntax_analysis.bnf_derivation.length > 0 && (
          <div className="mt-6">
            <h4 className="text-lg font-medium text-slate-900 dark:text-white mb-3">
              BNF Grammar Derivation
            </h4>
            <div className="bg-slate-100 dark:bg-slate-700/50 border border-slate-300 dark:border-slate-600 rounded-lg p-4">
              <div className="space-y-3">
                {result.syntax_analysis.bnf_derivation.map(
                  (derivation, index) => (
                    <div
                      key={index}
                      className="flex items-start gap-3 p-3 bg-white dark:bg-slate-800/50 rounded-lg border border-slate-200 dark:border-slate-600"
                    >
                      <span className="flex-shrink-0 w-8 h-8 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center text-sm font-medium">
                        {derivation.step}
                      </span>
                      <div className="flex-1">
                        <code className="text-slate-900 dark:text-white font-mono text-sm bg-slate-200 dark:bg-slate-700 px-2 py-1 rounded">
                          {derivation.rule}
                        </code>
                      </div>
                    </div>
                  ),
                )}
              </div>
            </div>
          </div>
        )}
    </div>
  );
}
