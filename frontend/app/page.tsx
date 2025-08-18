"use client";

import { useState } from "react";

// Interface for API result
interface Result {
  explanation: string;
  fileName: string;
  codeSnippet: string;
}

export default function Home() {
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
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-50">
      <div className="w-full max-w-2xl bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">
          AI Codebase Q&A Agent
        </h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="repoUrl"
              className="block text-sm font-medium text-gray-700"
            >
              GitHub Repository URL (Future Feature)
            </label>
            <input
              type="text"
              id="repoUrl"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              placeholder="https://github.com/example/repo"
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
          <div>
            <label
              htmlFor="question"
              className="block text-sm font-medium text-gray-700"
            >
              Your Question
            </label>
            <textarea
              id="question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., What does the 'get_order_details' function do?"
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              rows={3}
              required
            />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-300"
          >
            {isLoading ? "Asking..." : "Ask AI"}
          </button>
        </form>

        {/* Display Area for the Answer */}
        {result && (
          <div className="mt-8 p-4 border border-gray-200 rounded-lg bg-gray-50">
            <h2 className="text-lg font-semibold text-gray-900">Answer:</h2>
            <p className="mt-2 text-gray-700 whitespace-pre-wrap">
              {result.explanation}
            </p>
            <div className="mt-4">
              <p className="text-sm font-medium text-gray-600">
                {result.fileName}
              </p>
              <pre className="mt-1 p-3 bg-gray-900 text-white rounded-md text-sm overflow-x-auto">
                <code>{result.codeSnippet}</code>
              </pre>
            </div>
          </div>
        )}

        {/* Display Area for Errors */}
        {error && (
          <div className="mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-md">
            <p>
              <strong>Error:</strong> {error}
            </p>
          </div>
        )}
      </div>
    </main>
  );
}
