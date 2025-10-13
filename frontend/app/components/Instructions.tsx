"use client";

import { Code } from "lucide-react";

interface InstructionsProps {
  isVisible: boolean;
}

export default function Instructions({ isVisible }: InstructionsProps) {
  return (
    <div
      className={`bg-white/80 dark:bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 mb-8 border border-slate-200 dark:border-slate-700 shadow-lg fade-in fade-in-delay-1 ${isVisible ? "visible" : ""}`}
    >
      <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-6 flex items-center gap-2">
        <Code className="w-5 h-5 text-blue-500 dark:text-blue-400" />
        How to Use This Analyzer
      </h3>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h4 className="text-lg font-medium text-blue-600 dark:text-blue-400 mb-3">
            Supported Expressions
          </h4>
          <ul className="text-slate-700 dark:text-slate-300 space-y-2">
            <li className="break-all">
              •{" "}
              <code className="bg-slate-200 dark:bg-slate-700 px-2 py-1 rounded text-sm">
                int x = 5
              </code>{" "}
              - Variable declarations
            </li>
            <li className="break-all">
              •{" "}
              <code className="bg-slate-200 dark:bg-slate-700 px-2 py-1 rounded text-sm">
                double y = 3.14
              </code>{" "}
              - Different data types
            </li>
            <li className="break-all">
              •{" "}
              <code className="bg-slate-200 dark:bg-slate-700 px-2 py-1 rounded text-sm">
                x + y * 2
              </code>{" "}
              - Arithmetic expressions
            </li>
            <li className="break-all">
              •{" "}
              <code className="bg-slate-200 dark:bg-slate-700 px-2 py-1 rounded text-sm">
                if (x &gt; 0)
              </code>{" "}
              - Conditional statements
            </li>
            <li className="break-all">
              •{" "}
              <code className="bg-slate-200 dark:bg-slate-700 px-2 py-1 rounded text-sm">
                while (i &lt; 10)
              </code>{" "}
              - Loop constructs
            </li>
          </ul>
        </div>
        <div>
          <h4 className="text-lg font-medium text-blue-600 dark:text-blue-400 mb-3">
            Analysis Features
          </h4>
          <ul className="text-slate-700 dark:text-slate-300 space-y-2">
            <li>• Token breakdown and categorization</li>
            <li>• Grammar validation and syntax checking</li>
            <li>• Type checking and variable analysis</li>
            <li>• Comprehensive error detection</li>
            <li>• Variable declaration tracking</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
