"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { analyzeSample } from "@/lib/api";

export default function UploadCard() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [analysisId, setAnalysisId] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async () => {
    if (!file || isSubmitting) return;
    setIsSubmitting(true);
    setError(null);
    try {
      const result = await analyzeSample(file);
      setAnalysisId(result.analysis_id);
      router.push(`/reports/${result.analysis_id}`);
    } catch {
      setError("Failed to submit sample. Confirm backend is running.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="rounded-2xl bg-white p-6 shadow-sm">
      <h2 className="text-xl font-semibold mb-4">Upload Sample</h2>

      <input
        type="file"
        className="block w-full rounded-lg border border-slate-300 bg-slate-50 px-3 py-2 text-sm"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <button
        onClick={handleUpload}
        disabled={!file || isSubmitting}
        className="mt-4 rounded-xl bg-slate-900 px-4 py-2 text-white disabled:cursor-not-allowed disabled:opacity-60"
      >
        {isSubmitting ? "Submitting..." : "Analyze"}
      </button>
      {error && <p className="mt-3 text-sm text-red-600">{error}</p>}

      {analysisId && (
        <p className="mt-4 text-sm text-slate-700">
          Analysis ID: <span className="font-mono">{analysisId}</span>
        </p>
      )}
    </div>
  );
}
