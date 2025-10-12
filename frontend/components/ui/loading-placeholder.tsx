"use client";

import { Loader2 } from "lucide-react";

const LoadingPlaceholder = () => {
  return (
    <div className="space-y-6">
      {/* Status Overview Loading */}
      <div className="bg-white/80 dark:bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-200 dark:border-slate-700 shadow-lg">
        <div className="flex items-center gap-2 mb-4">
          <div className="h-7 bg-slate-200 dark:bg-slate-700 rounded w-48 animate-pulse"></div>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="flex items-center gap-3 p-4 bg-slate-100 dark:bg-slate-700/50 rounded-lg border border-slate-200 dark:border-slate-600"
            >
              <div className="w-6 h-6 bg-slate-300 dark:bg-slate-600 rounded-full animate-pulse"></div>
              <div className="flex-1">
                <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-20 mb-1 animate-pulse"></div>
                <div className="h-5 bg-slate-300 dark:bg-slate-600 rounded w-16 animate-pulse"></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Lexical Analysis Loading */}
      <div className="bg-white/80 dark:bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-200 dark:border-slate-700 shadow-lg">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-5 h-5 bg-slate-300 dark:bg-slate-600 rounded animate-pulse"></div>
          <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded w-36 animate-pulse"></div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b border-slate-300 dark:border-slate-600">
                <th className="text-left py-3 px-4">
                  <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-20 animate-pulse"></div>
                </th>
                <th className="text-left py-3 px-4">
                  <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-16 animate-pulse"></div>
                </th>
                <th className="text-left py-3 px-4">
                  <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-18 animate-pulse"></div>
                </th>
              </tr>
            </thead>
            <tbody>
              {[1, 2, 3, 4, 5].map((i) => (
                <tr
                  key={i}
                  className="border-b border-slate-200 dark:border-slate-700"
                >
                  <td className="py-3 px-4">
                    <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-24 animate-pulse"></div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-16 animate-pulse"></div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded w-20 animate-pulse"></div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Syntax Analysis Loading */}
      <div className="bg-white/80 dark:bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-200 dark:border-slate-700 shadow-lg">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-5 h-5 bg-slate-300 dark:bg-slate-600 rounded animate-pulse"></div>
          <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded w-32 animate-pulse"></div>
        </div>

        <div className="mb-4">
          <div className="flex items-center gap-2 p-4 rounded-lg border bg-slate-100 dark:bg-slate-700/50 border-slate-300 dark:border-slate-600">
            <div className="w-5 h-5 bg-slate-300 dark:bg-slate-600 rounded-full animate-pulse"></div>
            <div className="h-5 bg-slate-200 dark:bg-slate-700 rounded w-40 animate-pulse"></div>
          </div>
        </div>

        <div className="bg-slate-100 dark:bg-slate-700/50 border border-slate-300 dark:border-slate-600 rounded-lg p-4">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-slate-300 dark:bg-slate-600 rounded-full animate-pulse"></div>
            <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-48 animate-pulse"></div>
          </div>
        </div>
      </div>

      {/* Semantic Analysis Loading */}
      <div className="bg-white/80 dark:bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-200 dark:border-slate-700 shadow-lg">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-5 h-5 bg-slate-300 dark:bg-slate-600 rounded animate-pulse"></div>
          <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded w-36 animate-pulse"></div>
        </div>

        {/* Variables Declared Loading */}
        <div className="mb-6">
          <div className="h-5 bg-slate-200 dark:bg-slate-700 rounded w-32 mb-3 animate-pulse"></div>
          <div className="grid gap-3">
            {[1, 2].map((i) => (
              <div
                key={i}
                className="bg-slate-100 dark:bg-slate-700/50 rounded-lg p-4 border border-slate-200 dark:border-slate-600"
              >
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                  <div className="flex items-center gap-3">
                    <div className="h-5 bg-slate-200 dark:bg-slate-700 rounded w-12 animate-pulse"></div>
                    <div className="h-6 bg-slate-300 dark:bg-slate-600 rounded w-16 animate-pulse"></div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-14 animate-pulse"></div>
                    <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-20 animate-pulse"></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Semantic Analysis Result Loading */}
        <div className="bg-slate-100 dark:bg-slate-700/50 border border-slate-300 dark:border-slate-600 rounded-lg p-4">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-slate-300 dark:bg-slate-600 rounded-full animate-pulse"></div>
            <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-52 animate-pulse"></div>
          </div>
        </div>
      </div>

      {/* Loading Text */}
      <div className="text-center py-4">
        <div className="flex items-center justify-center gap-2 text-slate-600 dark:text-slate-400">
          <Loader2 className="w-5 h-5 animate-spin" />
          <span className="text-lg font-medium">
            Analyzing your expression...
          </span>
        </div>
        <p className="text-sm text-slate-500 dark:text-slate-500 mt-2">
          This may take a few seconds
        </p>
      </div>
    </div>
  );
};

export default LoadingPlaceholder;
