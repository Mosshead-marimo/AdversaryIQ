interface RiskGaugeProps {
  score: number;
}

const clamp = (value: number, min: number, max: number) =>
  Math.min(max, Math.max(min, value));

const gaugeColor = (score: number) => {
  if (score >= 75) return "#b91c1c";
  if (score >= 50) return "#dc2626";
  if (score >= 30) return "#d97706";
  return "#15803d";
};

export default function RiskGauge({ score }: RiskGaugeProps) {
  const safeScore = clamp(Number.isFinite(score) ? score : 0, 0, 100);
  const radius = 72;
  const circumference = Math.PI * radius;
  const progress = (safeScore / 100) * circumference;

  return (
    <section className="rounded-2xl bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold text-slate-900">Risk Score</h2>

      <div className="flex flex-col items-center justify-center">
        <svg viewBox="0 0 200 120" className="h-40 w-56" role="img" aria-label={`Risk score ${safeScore}`}>
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke="#e2e8f0"
            strokeWidth="16"
            strokeLinecap="round"
          />
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke={gaugeColor(safeScore)}
            strokeWidth="16"
            strokeLinecap="round"
            strokeDasharray={`${progress} ${circumference}`}
          />
          <text
            x="100"
            y="92"
            textAnchor="middle"
            className="fill-slate-900 text-3xl font-semibold"
          >
            {Math.round(safeScore)}
          </text>
          <text
            x="100"
            y="108"
            textAnchor="middle"
            className="fill-slate-500 text-xs"
          >
            / 100
          </text>
        </svg>
      </div>
    </section>
  );
}
