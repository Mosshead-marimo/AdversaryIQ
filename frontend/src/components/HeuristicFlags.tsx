import type { HeuristicFlag } from "@/types/report";

interface HeuristicFlagsProps {
  flags: HeuristicFlag[];
}

const severityClasses: Record<string, string> = {
  critical: "border border-red-300 bg-red-50 text-red-800",
  high: "border border-rose-300 bg-rose-50 text-rose-800",
  medium: "border border-amber-300 bg-amber-50 text-amber-800",
  low: "border border-emerald-300 bg-emerald-50 text-emerald-800",
};

export default function HeuristicFlags({ flags }: HeuristicFlagsProps) {
  return (
    <section className="rounded-2xl bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold text-slate-900">
        Heuristic Flags
      </h2>

      {flags.length === 0 && (
        <p className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
          No suspicious patterns detected.
        </p>
      )}

      <div className="space-y-3">
        {flags.map((flag, index) => {
          const severity = flag.severity.toLowerCase().trim();
          const classes =
            severityClasses[severity] ||
            "border border-slate-300 bg-slate-50 text-slate-800";

          return (
            <article
              key={`${flag.type}-${index}`}
              className={`rounded-xl p-4 ${classes}`}
            >
              <div className="flex items-center justify-between gap-3">
                <p className="font-semibold">{flag.type}</p>
                <span className="rounded-full bg-white/70 px-2 py-0.5 text-xs font-semibold uppercase tracking-wide">
                  {flag.severity}
                </span>
              </div>

              {flag.details && (
                <p className="mt-2 text-sm">
                  {Array.isArray(flag.details)
                    ? flag.details.join(", ")
                    : flag.details}
                </p>
              )}
            </article>
          );
        })}
      </div>
    </section>
  );
}
