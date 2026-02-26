"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import { AxiosError } from "axios";
import { fetchReport } from "@/lib/api";
import type { AnalysisReport } from "@/types/report";
import RiskBadge from "@/components/RiskBadge";
import RiskGauge from "@/components/RiskGauge";
import MitreTable from "@/components/MitreTable";
import AttackHeatmap from "@/components/AttackHeatmap";
import HeuristicFlags from "@/components/HeuristicFlags";
import ProcessTree from "@/components/ProcessTree";
import TimelineView from "@/components/TimelineView";

export default function ReportPage() {
  const params = useParams<{ id: string }>();
  const analysisId = params.id;
  const [report, setReport] = useState<AnalysisReport | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    const load = async () => {
      if (!analysisId) return;
      setIsLoading(true);
      setError(null);

      try {
        const response = await fetchReport(analysisId);
        if (isMounted) {
          setReport(response);
        }
      } catch (err) {
        if (isMounted) {
          if (err instanceof AxiosError) {
            setError(
              err.response?.data?.detail ||
                err.message ||
                "Unable to load analysis report.",
            );
          } else {
            setError("Unable to load analysis report.");
          }
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    void load();

    return () => {
      isMounted = false;
    };
  }, [analysisId]);

  const formattedRawJson = useMemo(() => {
    if (!report) return "";
    return JSON.stringify(report, null, 2);
  }, [report]);

  if (isLoading) {
    return (
      <main className="min-h-screen bg-slate-50 px-6 py-8 text-slate-900 md:px-10">
        <div className="mx-auto max-w-7xl rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
          <p className="text-sm text-slate-500">Loading report {analysisId}...</p>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="min-h-screen bg-slate-50 px-6 py-8 text-slate-900 md:px-10">
        <div className="mx-auto max-w-7xl rounded-2xl border border-red-200 bg-red-50 p-8 shadow-sm">
          <h1 className="text-lg font-semibold text-red-900">Failed to load report</h1>
          <p className="mt-2 text-sm text-red-700">{error}</p>
        </div>
      </main>
    );
  }

  if (!report) {
    return null;
  }

  const { risk_assessment, mitre_attack_analysis, advanced_behavior_analysis } = report;

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-8 text-slate-900 md:px-10">
      <div className="mx-auto max-w-7xl space-y-6">
        <header className="rounded-2xl bg-white p-6 shadow-sm">
          <p className="text-xs uppercase tracking-wide text-slate-500">PyDetonator Analysis Report</p>
          <div className="mt-2 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <h1 className="text-2xl font-semibold">Report ID: {analysisId}</h1>
            <RiskBadge classification={risk_assessment.classification} />
          </div>
        </header>

        <section className="grid grid-cols-1 gap-6 xl:grid-cols-3">
          <div className="xl:col-span-1">
            <RiskGauge score={risk_assessment.risk_score} />
          </div>
          <div className="space-y-6 xl:col-span-2">
            <AttackHeatmap tactics={mitre_attack_analysis.tactic_distribution} />
            <HeuristicFlags flags={advanced_behavior_analysis.heuristic_flags} />
          </div>
        </section>

        <section className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <MitreTable techniques={mitre_attack_analysis.mapped_techniques} />
          <TimelineView events={advanced_behavior_analysis.execution_timeline} />
        </section>

        <ProcessTree tree={advanced_behavior_analysis.process_tree} />

        <section className="rounded-2xl bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-lg font-semibold text-slate-900">Raw JSON</h2>
          <pre className="max-h-[30rem] overflow-auto rounded-xl bg-slate-950 p-4 text-xs text-slate-100">
            {formattedRawJson}
          </pre>
        </section>
      </div>
    </main>
  );
}
