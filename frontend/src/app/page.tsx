"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const router = useRouter();
  const [analysisId, setAnalysisId] = useState("");

  const openReport = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const normalized = analysisId.trim();
    if (!normalized) return;
    router.push(`/reports/${normalized}`);
  };

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-10 text-slate-900 md:px-10">
      <div className="mx-auto grid max-w-6xl gap-6 lg:grid-cols-[1.2fr_1fr]">
        <section className="rounded-2xl bg-gradient-to-br from-slate-900 via-slate-800 to-slate-700 p-8 text-slate-100 shadow-sm">
          <p className="text-xs uppercase tracking-[0.2em] text-slate-300">PyDetonator</p>
          <h1 className="mt-3 text-3xl font-semibold">Cyber Threat Analysis Dashboard</h1>
          <p className="mt-3 max-w-xl text-sm text-slate-300">
            Analyze suspicious files, inspect ATT&CK mappings, review behavioral indicators, and track process execution in one interface.
          </p>
          <div className="mt-6">
            <Link
              href="/analyze"
              className="inline-flex rounded-xl bg-red-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-red-500"
            >
              Submit New Analysis
            </Link>
          </div>
        </section>

        <section className="rounded-2xl bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold">Open Existing Report</h2>
          <p className="mt-1 text-sm text-slate-600">
            Enter a known analysis ID and open `/reports/{'{'}id{'}'}`.
          </p>
          <form onSubmit={openReport} className="mt-4 space-y-3">
            <input
              type="text"
              value={analysisId}
              onChange={(event) => setAnalysisId(event.target.value)}
              placeholder="e.g. 4fe622fd-..."
              className="w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 font-mono text-sm"
            />
            <button
              type="submit"
              className="w-full rounded-xl border border-slate-300 bg-slate-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-slate-800"
            >
              View Report
            </button>
          </form>
        </section>
      </div>
    </main>
  );
}
