"use client";

import { AnalysisResponse } from "../types/analysis";
import StatusOverview from "./StatusOverview";
import LexicalAnalysis from "./LexicalAnalysis";
import SyntaxAnalysis from "./SyntaxAnalysis";
import SemanticAnalysis from "./SemanticAnalysis";

interface AnalysisResultsProps {
  result: AnalysisResponse;
  onCopyJSON: () => void;
  copySuccess: boolean;
  isVisible: boolean;
}

export default function AnalysisResults({
  result,
  onCopyJSON,
  copySuccess,
  isVisible,
}: AnalysisResultsProps) {
  return (
    <div
      className={`space-y-6 fade-in fade-in-delay-2 ${isVisible ? "visible" : ""}`}
    >
      {/* Status Overview */}
      <StatusOverview
        result={result}
        onCopyJSON={onCopyJSON}
        copySuccess={copySuccess}
        isVisible={isVisible}
      />

      <LexicalAnalysis result={result} />

      <SyntaxAnalysis result={result} />

      <SemanticAnalysis result={result} />
    </div>
  );
}
