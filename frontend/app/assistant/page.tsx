"use client";

import { useState } from "react";

// Interface for API result
interface Result {
  explanation: string;
  fileName: string;
  codeSnippet: string;
}

export default function AssistantPage() {
  // GitHub repo URL
  const [repoUrl, setRepoUrl] = useState("");
  // User question
  const [question, setQuestion] = useState("");
  // JSON object result from API
  const [result, setResult] = useState<Result | null>(null);
  // Loading state
  const [isLoading, setIsLoading] = useState(false);
  // Error messages
  const [error, setError] = useState("");

  // Event handler for form submission
  const handleSubmit = async (e: React.FormEvent) => {
    // Prevent reload on form submission
    e.preventDefault();
    setIsLoading(true);
    setError("");
    setResult(null);

    try {
      const ingestResponse = await fetch("http://localhost:5000/ingest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo_url: repoUrl }),
      });

      if (!ingestResponse.ok) {
        const errData = await ingestResponse.json();
        throw new Error(
          errData.error || `Ingestion failed! status: ${ingestResponse.status}`
        );
      }
      console.log("Ingestion successful!");

      const res = await fetch("http://localhost:5000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: question }),
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.error || `HTTP error. status ${res.status}`);
      }

      const data: Result = await res.json();
      setResult(data);
    } catch (e: any) {
      setError(e.message || "An error occurred while processing your request.");
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="bg-neutral-900 min-h-screen">
      <div className="container mx-auto px-4 py-16">
        {/* Header Section */}
        <div className="max-w-4xl mx-auto text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-amber-50 mb-4">
            Your Codebase Assistant
          </h1>
          <p className="text-xl text-amber-100/80">
            Ask questions about any GitHub repository
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          {/* Input Form Card */}
          <div className="bg-neutral-800 rounded-2xl p-8 shadow-2xl border border-neutral-700 mb-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label
                  htmlFor="repoUrl"
                  className="block text-sm font-medium text-amber-100 mb-2"
                >
                  GitHub Repository URL
                </label>
                <input
                  type="text"
                  id="repoUrl"
                  value={repoUrl}
                  onChange={(e) => setRepoUrl(e.target.value)}
                  placeholder="https://github.com/example/repo"
                  className="w-full px-4 py-3 bg-neutral-700 border border-neutral-600 rounded-lg text-amber-50 placeholder-amber-100/50 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition-colors"
                />
              </div>

              <div>
                <label
                  htmlFor="question"
                  className="block text-sm font-medium text-amber-100 mb-2"
                >
                  Ask a Question
                </label>
                <textarea
                  id="question"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="e.g., What does the 'insert_order' function do?"
                  className="w-full px-4 py-3 bg-neutral-700 border border-neutral-600 rounded-lg text-amber-50 placeholder-amber-100/50 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition-colors resize-none"
                  rows={4}
                  required
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 disabled:from-amber-400 disabled:to-amber-500 text-neutral-900 font-semibold px-8 py-4 rounded-lg transition-all duration-200 transform hover:scale-102 shadow-lg disabled:transform-none disabled:shadow-md"
              >
                {isLoading ? "Processing..." : "Ask"}
              </button>
            </form>
          </div>

          {/* Results Section */}
          {result && (
            <div className="bg-neutral-800 rounded-2xl p-8 shadow-2xl border border-neutral-700 mb-8">
              <div className="flex items-center mb-6">
                <h2 className="text-2xl font-semibold text-amber-50">
                  Response:
                </h2>
              </div>

              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-medium text-amber-100 mb-3">
                    Explanation
                  </h3>
                  <p className="text-amber-50/90 leading-relaxed whitespace-pre-wrap bg-neutral-700/50 p-4 rounded-lg border border-neutral-600">
                    {result.explanation}
                  </p>
                </div>

                <div>
                  <h3 className="text-lg font-medium text-amber-100 mb-3">
                    Code Reference
                  </h3>
                  <div className="bg-neutral-900 rounded-lg border border-neutral-600 overflow-hidden">
                    <div className="px-4 py-2 bg-neutral-700/50 border-b border-neutral-600">
                      <span className="text-amber-400 text-sm font-mono">
                        {result.fileName}
                      </span>
                    </div>
                    <pre className="p-4 text-amber-50 text-sm overflow-x-auto">
                      <code>{result.codeSnippet}</code>
                    </pre>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Error Section */}
          {error && (
            <div className="bg-red-900/20 border border-red-700/50 rounded-2xl p-6 mb-8">
              <div className="flex items-center mb-2">
                <span className="text-red-400 text-xl mr-2">⚠️</span>
                <h3 className="text-lg font-medium text-red-400">Error</h3>
              </div>
              <p className="text-red-300">{error}</p>
            </div>
          )}

          {/* Background Decorations */}
          <div className="absolute top-1/4 right-10 w-20 h-20 bg-amber-500/5 rounded-full blur-xl"></div>
          <div className="absolute bottom-1/4 left-10 w-32 h-32 bg-amber-400/5 rounded-full blur-2xl"></div>
        </div>
      </div>
    </main>
  );
}
