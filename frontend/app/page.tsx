"use client";

import { useState } from "react";
import {
  CheckCircle,
  XCircle,
  Code,
  Zap,
  Brain,
  AlertTriangle,
} from "lucide-react";
import { ShineBorder } from "@/components/magicui/shine-border";

interface Token {
  category: string;
  lexeme: string | number;
  token_type: string;
}

interface Variable {
  initialized: boolean;
  line_no: number;
  type: string;
}

interface AnalysisResponse {
  input_expression: string;
  lexical_analysis: {
    tokens: Token[];
  };
  result_type: string;
  semantic_analysis: {
    errors: string[];
    variables_declared: Record<string, Variable>;
  };
  status: string;
  syntax_analysis: {
    accepted: boolean;
    errors?: string[];
  };
}

export default function Home() {
  const [expression, setExpression] = useState("");
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeExpression = async () => {
    if (!expression.trim()) {
      setError("Please enter an expression");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        "https://us-central1-cloudapi-465510.cloudfunctions.net/parse-expression",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ expression }),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      analyzeExpression();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <div className="min-h-screen p-4 sm:p-6 lg:p-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-6 sm:mb-8">
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-white mb-3 sm:mb-4">
              PROGRAM LANGUAGE ANALYZER
            </h1>
            <p className="text-gray-300 text-sm sm:text-base lg:text-lg mb-4 sm:mb-6 px-2">
              Real-time lexical, syntactic, and semantic validation for
              programming expressions
            </p>
          </div>

          {/* Instructions Section */}
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 sm:p-6 mb-6 sm:mb-8 border border-white/20">
            <h3 className="text-lg sm:text-xl font-bold text-white mb-3 sm:mb-4 flex items-center gap-2">
              How to Use This Analyzer
            </h3>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
              <div>
                <h4 className="text-base sm:text-lg font-semibold text-blue-300 mb-2 sm:mb-3">
                  Supported Expressions
                </h4>
                <ul className="text-gray-300 space-y-1 sm:space-y-2 text-xs sm:text-sm">
                  <li className="break-all">
                    •{" "}
                    <code className="bg-gray-700 px-1 sm:px-2 py-1 rounded text-xs">
                      int x = 5
                    </code>{" "}
                    - Variable declarations
                  </li>
                  <li className="break-all">
                    •{" "}
                    <code className="bg-gray-700 px-1 sm:px-2 py-1 rounded text-xs">
                      float y = 3.14
                    </code>{" "}
                    - Different data types
                  </li>
                  <li className="break-all">
                    •{" "}
                    <code className="bg-gray-700 px-1 sm:px-2 py-1 rounded text-xs">
                      x + y * 2
                    </code>{" "}
                    - Arithmetic expressions
                  </li>
                  <li className="break-all">
                    •{" "}
                    <code className="bg-gray-700 px-1 sm:px-2 py-1 rounded text-xs">
                      if (x &gt; 0)
                    </code>{" "}
                    - Conditional statements
                  </li>
                  <li className="break-all">
                    •{" "}
                    <code className="bg-gray-700 px-1 sm:px-2 py-1 rounded text-xs">
                      while (i &lt; 10)
                    </code>{" "}
                    - Loop constructs
                  </li>
                </ul>
              </div>
              <div>
                <h4 className="text-base sm:text-lg font-semibold text-green-300 mb-2 sm:mb-3">
                  What You'll Get
                </h4>
                <ul className="text-gray-300 space-y-1 sm:space-y-2 text-xs sm:text-sm">
                  <li>
                    • <span className="text-blue-300">Token breakdown</span> -
                    Each word/symbol identified
                  </li>
                  <li>
                    • <span className="text-green-300">Grammar validation</span>{" "}
                    - Syntax correctness check
                  </li>
                  <li>
                    • <span className="text-purple-300">Type checking</span> -
                    Variable and type analysis
                  </li>
                  <li>
                    • <span className="text-yellow-300">Error detection</span> -
                    Detailed error messages
                  </li>
                  <li>
                    • <span className="text-cyan-300">Variable tracking</span> -
                    Declaration and usage info
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Input Section */}
          <div className="relative bg-white/10 backdrop-blur-sm rounded-lg p-4 sm:p-6 mb-6 sm:mb-8 border border-white/20">
            <ShineBorder shineColor={["#A07CFE", "#FE8FB5", "#FFBE7B"]} />

            <label
              htmlFor="expression"
              className="block text-white text-base sm:text-lg font-medium mb-2 sm:mb-3"
            >
              Enter Your Programming Expression
            </label>
            <p className="text-gray-300 text-xs sm:text-sm mb-3 sm:mb-4">
              Type any programming language expression below and click "Analyze"
              to see the complete compilation analysis.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
              <input
                id="expression"
                type="text"
                value={expression}
                onChange={(e) => setExpression(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Try: int x = 5, float y = x * 2.5, if (x == 5), etc."
                className="flex-1 px-3 sm:px-4 py-2 sm:py-3 rounded-lg bg-white/20 text-white placeholder-gray-400 border border-white/30 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all duration-200 text-sm sm:text-base"
              />
              <button
                onClick={analyzeExpression}
                disabled={loading}
                className="px-6 sm:px-8 py-2 sm:py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium rounded-lg transition-colors flex items-center justify-center gap-2 text-sm sm:text-base min-w-[120px] sm:min-w-[140px]"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    <span className="hidden sm:inline">Analyzing...</span>
                    <span className="sm:hidden">...</span>
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4" />
                    Analyze
                  </>
                )}
              </button>
            </div>
            {error && (
              <p className="text-red-400 mt-3 flex items-center gap-2 text-sm">
                <AlertTriangle className="w-4 h-4 flex-shrink-0" />
                <span className="break-words">{error}</span>
              </p>
            )}
          </div>

          {/* Results Section */}
          {!result && !loading && (
            <div className="bg-gradient-to-r from-green-600/10 to-blue-600/10 backdrop-blur-sm rounded-lg p-4 sm:p-6 border border-green-400/20">
              <h3 className="text-lg sm:text-xl font-bold text-white mb-3 sm:mb-4 flex items-center gap-2">
                Quick Start Guide
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4">
                <div className="bg-white/5 rounded-lg p-3 sm:p-4 border border-white/10">
                  <h4 className="text-blue-300 font-semibold mb-2 text-sm sm:text-base">
                    1. Lexical Analysis
                  </h4>
                  <p className="text-gray-300 text-xs sm:text-sm">
                    Breaks down your expression into tokens (keywords,
                    identifiers, operators, literals)
                  </p>
                </div>
                <div className="bg-white/5 rounded-lg p-3 sm:p-4 border border-white/10">
                  <h4 className="text-green-300 font-semibold mb-2 text-sm sm:text-base">
                    2. Syntax Analysis
                  </h4>
                  <p className="text-gray-300 text-xs sm:text-sm">
                    Checks if your expression follows proper grammar rules and
                    structure
                  </p>
                </div>
                <div className="bg-white/5 rounded-lg p-3 sm:p-4 border border-white/10">
                  <h4 className="text-purple-300 font-semibold mb-2 text-sm sm:text-base">
                    3. Semantic Analysis
                  </h4>
                  <p className="text-gray-300 text-xs sm:text-sm">
                    Validates types, variable declarations, and logical
                    consistency
                  </p>
                </div>
              </div>
              <div className="mt-3 sm:mt-4 p-3 sm:p-4 bg-yellow-600/10 border border-yellow-400/20 rounded-lg">
                <p className="text-yellow-300 text-xs sm:text-sm">
                  💡 <strong>Tip:</strong> Start with simple expressions like
                  "int x = 5" to see how the analyzer works, then try more
                  complex ones!
                </p>
              </div>
            </div>
          )}

          {result && (
            <div className="space-y-4 sm:space-y-6">
              {/* Status Overview */}
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 sm:p-6 border border-white/20">
                <h2 className="text-xl sm:text-2xl font-bold text-white mb-3 sm:mb-4 flex items-center gap-2">
                  Analysis Results
                </h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
                  <div className="flex items-center gap-2 sm:gap-3 p-3 bg-white/5 rounded-lg">
                    {result.status === "success" ? (
                      <CheckCircle className="w-5 h-5 sm:w-6 sm:h-6 text-green-400 flex-shrink-0" />
                    ) : (
                      <XCircle className="w-5 h-5 sm:w-6 sm:h-6 text-red-400 flex-shrink-0" />
                    )}
                    <div className="min-w-0">
                      <p className="text-xs sm:text-sm text-gray-300">Overall Status</p>
                      <p className="text-sm sm:text-base text-white font-medium capitalize truncate">
                        {result.status}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 sm:gap-3 p-3 bg-white/5 rounded-lg">
                    {result.syntax_analysis.accepted ? (
                      <CheckCircle className="w-5 h-5 sm:w-6 sm:h-6 text-green-400 flex-shrink-0" />
                    ) : (
                      <XCircle className="w-5 h-5 sm:w-6 sm:h-6 text-red-400 flex-shrink-0" />
                    )}
                    <div className="min-w-0">
                      <p className="text-xs sm:text-sm text-gray-300">Syntax Analysis</p>
                      <p className="text-sm sm:text-base text-white font-medium truncate">
                        {result.syntax_analysis.accepted
                          ? "Accepted"
                          : "Rejected"}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 sm:gap-3 p-3 bg-white/5 rounded-lg sm:col-span-2 lg:col-span-1">
                    {result.semantic_analysis.errors.length === 0 ? (
                      <CheckCircle className="w-5 h-5 sm:w-6 sm:h-6 text-green-400 flex-shrink-0" />
                    ) : (
                      <XCircle className="w-5 h-5 sm:w-6 sm:h-6 text-red-400 flex-shrink-0" />
                    )}
                    <div className="min-w-0">
                      <p className="text-xs sm:text-sm text-gray-300">Semantic Analysis</p>
                      <p className="text-sm sm:text-base text-white font-medium truncate">
                        {result.semantic_analysis.errors.length === 0
                          ? "No Errors"
                          : `${result.semantic_analysis.errors.length} Error(s)`}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Lexical Analysis */}
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 sm:p-6 border border-white/20">
                <h3 className="text-lg sm:text-xl font-bold text-white mb-3 sm:mb-4 flex items-center gap-2">
                  <Code className="w-4 h-4 sm:w-5 sm:h-5" />
                  Lexical Analysis
                </h3>
                <div className="overflow-x-auto -mx-4 sm:mx-0">
                  <div className="min-w-full px-4 sm:px-0">
                    <table className="w-full border-collapse min-w-[500px]">
                      <thead>
                        <tr className="border-b border-white/20">
                          <th className="text-left py-2 sm:py-3 px-2 sm:px-4 text-white font-medium text-sm sm:text-base">
                            Token Type
                          </th>
                          <th className="text-left py-2 sm:py-3 px-2 sm:px-4 text-white font-medium text-sm sm:text-base">
                            Lexeme
                          </th>
                          <th className="text-left py-2 sm:py-3 px-2 sm:px-4 text-white font-medium text-sm sm:text-base">
                            Category
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {result.lexical_analysis.tokens.map((token, index) => (
                          <tr
                            key={index}
                            className="border-b border-white/10 hover:bg-white/5"
                          >
                            <td className="py-2 sm:py-3 px-2 sm:px-4 text-gray-300 font-mono text-xs sm:text-sm break-all">
                              {token.token_type}
                            </td>
                            <td className="py-2 sm:py-3 px-2 sm:px-4 text-white font-mono text-xs sm:text-sm break-all">
                              {token.lexeme}
                            </td>
                            <td className="py-2 sm:py-3 px-2 sm:px-4 text-gray-300">
                              <span
                                className={`px-1 sm:px-2 py-1 rounded text-xs font-medium ${
                                  token.category === "Keywords"
                                    ? "bg-blue-600/20 text-blue-300"
                                    : token.category === "Identifier"
                                    ? "bg-green-600/20 text-green-300"
                                    : token.category === "Operator"
                                    ? "bg-yellow-600/20 text-yellow-300"
                                    : token.category === "Literal"
                                    ? "bg-purple-600/20 text-purple-300"
                                    : "bg-gray-600/20 text-gray-300"
                                }`}
                              >
                                {token.category}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              {/* Syntax Analysis */}
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 sm:p-6 border border-white/20">
                <h3 className="text-lg sm:text-xl font-bold text-white mb-3 sm:mb-4 flex items-center gap-2">
                  <Code className="w-4 h-4 sm:w-5 sm:h-5" />
                  Syntax Analysis
                </h3>

                {/* Syntax Status */}
                <div className="mb-3 sm:mb-4">
                  <div
                    className={`flex items-center gap-2 p-3 rounded-lg ${
                      result.syntax_analysis.accepted
                        ? "bg-green-600/10 border border-green-600/20"
                        : "bg-red-600/10 border border-red-600/20"
                    }`}
                  >
                    {result.syntax_analysis.accepted ? (
                      <>
                        <CheckCircle className="w-4 h-4 sm:w-5 sm:h-5 text-green-400 flex-shrink-0" />
                        <span className="text-green-400 font-medium text-sm sm:text-base">
                          Syntax is valid
                        </span>
                      </>
                    ) : (
                      <>
                        <XCircle className="w-4 h-4 sm:w-5 sm:h-5 text-red-400 flex-shrink-0" />
                        <span className="text-red-400 font-medium text-sm sm:text-base">
                          Syntax errors detected
                        </span>
                      </>
                    )}
                  </div>
                </div>

                {/* Syntax Errors */}
                {result.syntax_analysis.errors &&
                result.syntax_analysis.errors.length > 0 ? (
                  <div>
                    <h4 className="text-base sm:text-lg font-medium text-white mb-2 sm:mb-3">
                      Syntax Errors
                    </h4>
                    <div className="space-y-2">
                      {result.syntax_analysis.errors.map((error, index) => (
                        <div
                          key={index}
                          className="bg-red-600/10 border border-red-600/20 rounded-lg p-3"
                        >
                          <p className="text-red-400 flex items-start gap-2 text-sm sm:text-base">
                            <XCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                            <span className="break-words">{error}</span>
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : result.syntax_analysis.accepted ? (
                  <div className="bg-green-600/10 border border-green-600/20 rounded-lg p-3 sm:p-4">
                    <p className="text-green-400 flex items-center gap-2 text-sm sm:text-base">
                      <CheckCircle className="w-4 h-4 flex-shrink-0" />
                      No syntax errors found
                    </p>
                  </div>
                ) : (
                  <div className="bg-yellow-600/10 border border-yellow-600/20 rounded-lg p-3 sm:p-4">
                    <p className="text-yellow-400 flex items-center gap-2 text-sm sm:text-base">
                      <AlertTriangle className="w-4 h-4 flex-shrink-0" />
                      Syntax analysis failed - check your expression
                    </p>
                  </div>
                )}
              </div>

              {/* Semantic Analysis */}
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 sm:p-6 border border-white/20">
                <h3 className="text-lg sm:text-xl font-bold text-white mb-3 sm:mb-4 flex items-center gap-2">
                  <Brain className="w-4 h-4 sm:w-5 sm:h-5" />
                  Semantic Analysis
                </h3>

                {/* Variables Declared */}
                {Object.keys(result.semantic_analysis.variables_declared)
                  .length > 0 && (
                  <div className="mb-4 sm:mb-6">
                    <h4 className="text-base sm:text-lg font-medium text-white mb-2 sm:mb-3">
                      Variables Declared
                    </h4>
                    <div className="grid gap-2 sm:gap-3">
                      {Object.entries(
                        result.semantic_analysis.variables_declared
                      ).map(([name, variable]) => (
                        <div
                          key={name}
                          className="bg-white/5 rounded-lg p-3 sm:p-4 border border-white/10"
                        >
                          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 sm:gap-0">
                            <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-3">
                              <span className="text-white font-mono text-sm sm:text-lg break-all">
                                {name}
                              </span>
                              <span className="px-2 py-1 bg-blue-600/20 text-blue-300 rounded text-xs font-medium w-fit">
                                {variable.type}
                              </span>
                            </div>
                            <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 text-xs sm:text-sm">
                              <span className="text-gray-300">
                                Line {variable.line_no}
                              </span>
                              <span
                                className={`flex items-center gap-1 w-fit ${
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
                      ))}
                    </div>
                  </div>
                )}

                {/* Semantic Errors */}
                {result.semantic_analysis.errors.length > 0 ? (
                  <div>
                    <h4 className="text-base sm:text-lg font-medium text-white mb-2 sm:mb-3">
                      Semantic Errors
                    </h4>
                    <div className="space-y-2">
                      {result.semantic_analysis.errors.map((error, index) => (
                        <div
                          key={index}
                          className="bg-red-600/10 border border-red-600/20 rounded-lg p-3"
                        >
                          <p className="text-red-400 flex items-start gap-2 text-sm sm:text-base">
                            <XCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                            <span className="break-words">{error}</span>
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="bg-green-600/10 border border-green-600/20 rounded-lg p-3 sm:p-4">
                    <p className="text-green-400 flex items-center gap-2 text-sm sm:text-base">
                      <CheckCircle className="w-4 h-4 flex-shrink-0" />
                      No semantic errors found
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="max-w-6xl mx-auto mt-8 sm:mt-12">
          <div className="text-center py-4 sm:py-6 border-t border-white/20 px-4">
            <p className="text-gray-400 text-xs sm:text-sm">
              Programming Language Compiler Design Final Project<br />Built with Next.js, TypeScript, and Python
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
