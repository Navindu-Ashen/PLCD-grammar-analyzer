"use client";

import { CheckCircle, XCircle, Copy } from "lucide-react";
import { AnalysisResponse } from "../types/analysis";

interface StatusOverviewProps {
  result: AnalysisResponse;
  onCopyJSON: () => void;
  copySuccess: boolean;
  isVisible: boolean;
}

export default function StatusOverview({
  result,
  onCopyJSON,
  copySuccess,
  isVisible,
}: StatusOverviewProps) {
  return (
    <div className="bg-white/80 dark:bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-200 dark:border-slate-700 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <CheckCircle className="w-6 h-6 text-blue-500 dark:text-blue-400" />
          Analysis Results
        </h2>
        <button
          onClick={onCopyJSON}
          className={`flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors border ${
            copySuccess
              ? "bg-green-200 hover:bg-green-300 dark:bg-green-800 dark:hover:bg-green-700 text-green-800 dark:text-green-200 border-green-300 dark:border-green-600"
              : "bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-600 hover:border-slate-400 dark:hover:border-slate-500"
          }`}
          title="Copy response JSON to clipboard"
        >
          <Copy className="w-4 h-4" />
          {copySuccess ? "Copied!" : "Copy JSON"}
        </button>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="flex items-center gap-3 p-4 bg-slate-100 dark:bg-slate-700/50 rounded-lg border border-slate-200 dark:border-slate-600">
          {result.status === "success" ? (
            <CheckCircle className="w-6 h-6 text-green-400 flex-shrink-0" />
          ) : (
            <XCircle className="w-6 h-6 text-red-400 flex-shrink-0" />
          )}
          <div>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Overall Status
            </p>
            <p className="text-slate-900 dark:text-white font-medium capitalize">
              {result.status}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3 p-4 bg-slate-100 dark:bg-slate-700/50 rounded-lg border border-slate-200 dark:border-slate-600">
          {result.syntax_analysis.accepted ? (
            <CheckCircle className="w-6 h-6 text-green-400 flex-shrink-0" />
          ) : (
            <XCircle className="w-6 h-6 text-red-400 flex-shrink-0" />
          )}
          <div>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Syntax Analysis
            </p>
            <p className="text-slate-900 dark:text-white font-medium">
              {result.syntax_analysis.accepted ? "Accepted" : "Rejected"}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3 p-4 bg-slate-100 dark:bg-slate-700/50 rounded-lg border border-slate-200 dark:border-slate-600">
          {result.semantic_analysis.errors.length === 0 ? (
            <CheckCircle className="w-6 h-6 text-green-400 flex-shrink-0" />
          ) : (
            <XCircle className="w-6 h-6 text-red-400 flex-shrink-0" />
          )}
          <div>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Semantic Analysis
            </p>
            <p className="text-slate-900 dark:text-white font-medium">
              {result.semantic_analysis.errors.length === 0
                ? "No Errors"
                : `${result.semantic_analysis.errors.length} Error(s)`}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
