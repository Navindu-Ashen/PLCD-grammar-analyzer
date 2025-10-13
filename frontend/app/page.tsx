"use client";

import { useState, useEffect, useRef } from "react";
import { AnalysisResponse } from "./types/analysis";
import SplashScreen from "./components/SplashScreen";
import Header from "./components/Header";
import Instructions from "./components/Instructions";
import InputSection from "./components/InputSection";
import AnalysisProcess from "./components/AnalysisProcess";
import AnalysisResults from "./components/AnalysisResults";
import Footer from "./components/Footer";
import LoadingPlaceholder from "@/components/ui/loading-placeholder";
import { LightRays } from "@/components/ui/light-rays";

export default function Home() {
  const [expression, setExpression] = useState("");
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showSplash, setShowSplash] = useState(true);
  const [copySuccess, setCopySuccess] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const inputSectionRef = useRef<HTMLElement>(null);

  const copyToClipboard = async () => {
    if (!result) return;

    try {
      await navigator.clipboard.writeText(JSON.stringify(result, null, 2));
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    } catch (err) {
      console.error("Failed to copy to clipboard:", err);
    }
  };

  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    const systemTheme = window.matchMedia("(prefers-color-scheme: dark)")
      .matches
      ? "dark"
      : "light";
    const theme = savedTheme || systemTheme;

    if (theme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, []);

  const analyzeExpression = async () => {
    if (!expression.trim()) {
      setError("Please enter an expression");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        "https://us-central1-uni-projects-472705.cloudfunctions.net/parse-expression",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ expression }),
        },
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);

      setTimeout(() => {
        inputSectionRef.current?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }, 100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleSplashComplete = () => {
    setShowSplash(false);
    setTimeout(() => setIsVisible(true), 100);
  };

  if (showSplash) {
    return <SplashScreen onComplete={handleSplashComplete} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 transition-colors duration-300">
      <div className="min-h-screen p-4 sm:p-6 lg:p-8">
        <div className="max-w-6xl mx-auto">
          <Header isVisible={isVisible} />

          <Instructions isVisible={isVisible} />

          <InputSection
            ref={inputSectionRef}
            expression={expression}
            setExpression={setExpression}
            onAnalyze={analyzeExpression}
            loading={loading}
            error={error}
            isVisible={isVisible}
          />

          {!result && !loading && <AnalysisProcess isVisible={isVisible} />}

          {loading && <LoadingPlaceholder />}

          {result && (
            <AnalysisResults
              result={result}
              onCopyJSON={copyToClipboard}
              copySuccess={copySuccess}
              isVisible={isVisible}
            />
          )}
        </div>

        <Footer isVisible={isVisible} />
      </div>
    </div>
  );
}
