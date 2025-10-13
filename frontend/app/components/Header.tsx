"use client";

import { AnimatedThemeToggler } from "@/components/ui/animated-theme-toggler";

interface HeaderProps {
  isVisible: boolean;
}

export default function Header({ isVisible }: HeaderProps) {
  return (
    <>
      <div
        className={`absolute top-4 right-4 fade-in fade-in-delay-1 ${isVisible ? "visible" : ""}`}
      >
        <AnimatedThemeToggler className="" />
      </div>

      <div className={`text-center my-8 fade-in ${isVisible ? "visible" : ""}`}>
        <h1 className="text-3xl sm:text-4xl mb-2 uppercase lg:text-5xl font-bold text-slate-900 dark:text-white">
          Program Language Analyzer
        </h1>
        <p className="text-slate-600 dark:text-slate-400 text-lg">
          Advanced lexical, syntactic, and semantic validation for programming
          expressions
        </p>
        <p className="text-slate-600 dark:text-slate-400 text-lg mb-6">
          By<strong> Group V</strong>
        </p>
      </div>
    </>
  );
}
