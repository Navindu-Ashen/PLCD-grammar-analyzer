"use client";

import { useState, useEffect } from "react";
import Image from "next/image";
import { Loader2 } from "lucide-react";

interface SplashScreenProps {
  onComplete: () => void;
}

export default function SplashScreen({ onComplete }: SplashScreenProps) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setTimeout(onComplete, 500);
          return 100;
        }
        return prev + 2;
      });
    }, 30);

    return () => clearInterval(interval);
  }, [onComplete]);

  return (
    <div className="fixed inset-0 bg-slate-900 dark:bg-slate-900 flex items-center justify-center z-50">
      <div className="text-center space-y-8">
        <div className="space-y-4">
          <div className="relative mx-auto w-24 h-24">
            <div className="absolute inset-0 border-4 border-slate-700 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-blue-500 rounded-full border-t-transparent animate-spin"></div>
            <div className="absolute inset-2 bg-blue-500/20 rounded-full flex items-center justify-center">
              <Image
                src="/code-review-2E.png"
                className="p-2"
                alt="Logo"
                width={64}
                height={64}
              />
            </div>
          </div>

          <div className="space-y-2">
            <h1 className="text-3xl font-bold text-white">
              Program Language Analyzer
            </h1>
            <p className="text-slate-400">
              Initializing compiler components...
            </p>
          </div>

          <p className="absolute bottom-12 left-0 right-0 mx-auto text-slate-400">
            By <strong>Group V</strong>
          </p>
        </div>
      </div>
    </div>
  );
}
