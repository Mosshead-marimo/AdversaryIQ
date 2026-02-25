interface AttackHeatmapProps {
  tactics: Record<string, number>;
}

const colorByIntensity = (value: number, max: number) => {
  if (max === 0 || value === 0) {
    return "bg-slate-100 text-slate-500 border border-slate-200";
  }

  const ratio = value / max;
  if (ratio >= 0.8) return "bg-red-700 text-red-50";
  if (ratio >= 0.6) return "bg-red-600 text-red-50";
  if (ratio >= 0.4) return "bg-orange-500 text-orange-50";
  if (ratio >= 0.2) return "bg-amber-400 text-amber-950";
  return "bg-lime-300 text-lime-950";
};

export default function AttackHeatmap({
  tactics,
}: AttackHeatmapProps) {
  const entries = Object.entries(tactics);
  const max = Math.max(0, ...entries.map(([, count]) => count));

  return (
    <section className="rounded-2xl bg-white p-6 shadow-sm">
      <div className="mb-4 flex items-center justify-between gap-3">
        <h2 className="text-lg font-semibold text-slate-900">
          ATT&CK Tactic Heatmap
        </h2>
        <span className="text-xs text-slate-500">
          Based on tactic distribution
        </span>
      </div>

      {entries.length === 0 ? (
        <p className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
          No tactic distribution returned by backend.
        </p>
      ) : (
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">
          {entries
            .sort(([a], [b]) => a.localeCompare(b))
            .map(([tactic, count]) => (
              <div
                key={tactic}
                className={`rounded-xl p-4 ${colorByIntensity(
                  count,
                  max,
                )}`}
              >
                <p className="text-xs uppercase tracking-wide opacity-90">
                  {tactic.replaceAll("_", " ")}
                </p>
                <p className="mt-1 text-2xl font-semibold">{count}</p>
              </div>
            ))}
        </div>
      )}
    </section>
  );
}
