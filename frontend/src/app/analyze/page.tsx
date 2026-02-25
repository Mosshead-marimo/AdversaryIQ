"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { analyzeSample } from "@/lib/api";

export default function AnalyzePage() {
  const router = useRouter();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [analysisId, setAnalysisId] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!selectedFile || isSubmitting) {
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const response = await analyzeSample(selectedFile);
      setAnalysisId(response.analysis_id);
      setTimeout(() => {
        router.push(`/reports/${response.analysis_id}`);
      }, 800);
    } catch {
      setError(
        "Could not submit file for analysis. Ensure backend API is reachable.",
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-10 text-slate-900 md:px-10">
      <div className="mx-auto max-w-3xl space-y-6">
        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <p className="text-xs uppercase tracking-wide text-slate-500">PyDetonator</p>
          <h1 className="mt-2 text-2xl font-semibold">Submit Sample for Dynamic Analysis</h1>
          <p className="mt-2 text-sm text-slate-600">
            Upload an executable sample to start analysis via the `/analyze` endpoint.
          </p>
        </div>

        <form onSubmit={onSubmit} className="rounded-2xl bg-white p-6 shadow-sm">
          <label className="block text-sm font-medium text-slate-700">Sample File</label>
          <input
            type="file"
            onChange={(event) => setSelectedFile(event.target.files?.[0] || null)}
            className="mt-2 block w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm"
            required
          />

          <div className="mt-5 flex flex-wrap items-center gap-3">
            <button
              type="submit"
              disabled={!selectedFile || isSubmitting}
              className="rounded-xl bg-slate-900 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isSubmitting ? "Submitting..." : "Analyze Sample"}
            </button>
            <Link
              href="/"
              className="rounded-xl border border-slate-300 px-5 py-2.5 text-sm font-medium text-slate-700 transition hover:bg-slate-100"
            >
              Back to Dashboard
            </Link>
          </div>

          {analysisId && (
            <p className="mt-4 text-sm text-slate-700">
              Analysis started with ID: <span className="font-mono">{analysisId}</span>
            </p>
          )}

          {error && <p className="mt-4 text-sm text-red-600">{error}</p>}
        </form>
      </div>
    </main>
  );
}
