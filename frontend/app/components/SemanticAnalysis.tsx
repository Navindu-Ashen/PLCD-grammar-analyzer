"use client";

import { Brain, CheckCircle, XCircle, AlertTriangle } from "lucide-react";
import { AnalysisResponse } from "../types/analysis";

interface SemanticAnalysisProps {
  result: AnalysisResponse;
}

export default function SemanticAnalysis({ result }: SemanticAnalysisProps) {
  return (
    <div className="bg-white/80 dark:bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-200 dark:border-slate-700 shadow-lg">
      <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
        <Brain className="w-5 h-5 text-blue-500 dark:text-blue-400" />
        Semantic Analysis
      </h3>

      {Object.keys(result.semantic_analysis.variables_declared).length > 0 && (
        <div className="mb-6">
          <h4 className="text-lg font-medium text-slate-900 dark:text-white mb-3">
            Variables Declared
          </h4>
          <div className="grid gap-3">
            {Object.entries(result.semantic_analysis.variables_declared).map(
              ([name, variable]) => (
                <div
                  key={name}
                  className="bg-slate-100 dark:bg-slate-700/50 rounded-lg p-4 border border-slate-200 dark:border-slate-600"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                    <div className="flex items-center gap-3">
                      <span className="text-slate-900 dark:text-white font-mono text-lg">
                        {name}
                      </span>
                      <span className="px-2 py-1 bg-blue-200 dark:bg-blue-600/20 text-blue-800 dark:text-blue-300 rounded text-sm font-medium">
                        {variable.type}
                      </span>
                    </div>
                    <div className="flex items-center gap-4 text-sm">
                      <span className="text-slate-600 dark:text-slate-400">
                        Line {variable.line_no}
                      </span>
                      <span
                        className={`flex items-center gap-1 ${
                          variable.initialized
                            ? "text-green-400"
                            : "text-yellow-400"
                        }`}
                      >
                        {variable.initialized ? (
                          <>
                            <CheckCircle className="w-3 h-3" />
                            Initialized
                          </>
                        ) : (
                          <>
                            <AlertTriangle className="w-3 h-3" />
                            Not Initialized
                          </>
                        )}
                      </span>
                    </div>
                  </div>
                </div>
              )
            )}
          </div>
        </div>
      )}

      {result.semantic_analysis.errors.length > 0 ? (
        <div>
          <h4 className="text-lg font-medium text-slate-900 dark:text-white mb-3">
            Semantic Errors
          </h4>
          <div className="space-y-2">
            {result.semantic_analysis.errors.map((error, index) => (
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
      ) : (
        <div className="bg-green-100 dark:bg-green-900/20 border border-green-300 dark:border-green-700 rounded-lg p-4">
          <p className="text-green-700 dark:text-green-400 flex items-center gap-2">
            <CheckCircle className="w-4 h-4 flex-shrink-0" />
            No semantic errors found
          </p>
        </div>
      )}
    </div>
  );
}
