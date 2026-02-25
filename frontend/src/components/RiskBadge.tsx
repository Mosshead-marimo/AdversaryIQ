interface RiskBadgeProps {
  classification: string;
}

const normalize = (value: string) => value.toLowerCase().trim();

export default function RiskBadge({ classification }: RiskBadgeProps) {
  const value = normalize(classification);

  let classes =
    "border border-emerald-300 bg-emerald-100 text-emerald-800";

  if (value.includes("malicious") || value.includes("critical")) {
    classes = "border border-red-300 bg-red-100 text-red-800";
  } else if (
    value.includes("suspicious") ||
    value.includes("medium") ||
    value.includes("high")
  ) {
    classes =
      "border border-amber-300 bg-amber-100 text-amber-800";
  }

  return (
    <span
      className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wide ${classes}`}
    >
      {classification}
    </span>
  );
}
