"use client";

import { TypingAnimation } from "@/components/magicui/typing-animation";
import { AuroraText } from "@/components/magicui/aurora-text";
import Link from "next/link";

export default function Home() {
  return (
    <main className="bg-neutral-900 min-h-screen">
      <div className="container mx-auto px-4 py-16">
        {/* Simple Hero Card */}
        <div className="max-w-3xl mx-auto text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-amber-50 mb-8">
            Welcome to{" "}
            <AuroraText
              colors={[
                "#D97706",
                "#F59E0B",
                "#FCD34D",
                "#F97316",
                "#DC2626",
                "#FBBF24",
              ]}
              speed={1.5}
            >
              ProgAssist
            </AuroraText>
          </h1>
          <TypingAnimation
            startOnView={true}
            className="text-2xl font-semibold text-amber-50"
          >
            Your AI-powered codebase assistant
          </TypingAnimation>
        </div>

        {/* Main Features Section */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-neutral-800 rounded-2xl p-12 shadow-2xl border border-neutral-700 backdrop-blur-sm">
            {/* Badge */}
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-8 mx-auto">
              <div className="w-2 h-2 bg-amber-400 rounded-full mr-2 animate-pulse"></div>
              <span className="text-amber-400 text-sm font-medium">
                AI-Powered Assistant
              </span>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
              <div className="bg-neutral-700/50 rounded-lg p-6 border border-neutral-600">
                <div className="w-12 h-12 bg-amber-500/20 rounded-lg flex items-center justify-center mb-4 mx-auto">
                  <span className="text-amber-400 text-xl">🤖</span>
                </div>
                <h3 className="text-amber-50 font-semibold mb-2">
                  Smart Analysis
                </h3>
                <p className="text-amber-100/70 text-sm">
                  Powered by Google's Gemini LLM
                </p>
              </div>

              <div className="bg-neutral-700/50 rounded-lg p-6 border border-neutral-600">
                <div className="w-12 h-12 bg-amber-500/20 rounded-lg flex items-center justify-center mb-4 mx-auto">
                  <span className="text-amber-400 text-xl">⚡</span>
                </div>
                <h3 className="text-amber-50 font-semibold mb-2">
                  Fast Navigation
                </h3>
                <p className="text-amber-100/70 text-sm">
                  Quickly find and understand code patterns
                </p>
              </div>

              <div className="bg-neutral-700/50 rounded-lg p-6 border border-neutral-600">
                <div className="w-12 h-12 bg-amber-500/20 rounded-lg flex items-center justify-center mb-4 mx-auto">
                  <span className="text-amber-400 text-xl">💡</span>
                </div>
                <h3 className="text-amber-50 font-semibold mb-2">
                  Smart Insights
                </h3>
                <p className="text-amber-100/70 text-sm">
                  Get contextual insights about your codebase
                </p>
              </div>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link
                href="/assistant"
                className="bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-neutral-900 font-semibold px-8 py-3 rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg inline-block"
              >
                Get Started
              </Link>
            </div>
          </div>

          {/* Background Decorations */}
          <div className="absolute top-1/4 left-10 w-20 h-20 bg-amber-500/5 rounded-full blur-xl"></div>
          <div className="absolute bottom-1/4 right-10 w-32 h-32 bg-amber-400/5 rounded-full blur-2xl"></div>
        </div>
      </div>
    </main>
  );
}
