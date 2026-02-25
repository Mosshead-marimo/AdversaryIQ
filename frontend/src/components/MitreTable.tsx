import type { MitreTechnique } from "@/types/report";

interface MitreTableProps {
  techniques: MitreTechnique[];
}

export default function MitreTable({ techniques }: MitreTableProps) {
  return (
    <section className="rounded-2xl bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold text-slate-900">
        MITRE ATT&CK Techniques
      </h2>

      {techniques.length === 0 ? (
        <p className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
          No mapped techniques found.
        </p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500">
                <th className="px-3 py-2 font-medium">Technique ID</th>
                <th className="px-3 py-2 font-medium">Technique</th>
                <th className="px-3 py-2 font-medium">Evidence</th>
              </tr>
            </thead>
            <tbody>
              {techniques.map((technique) => (
                <tr
                  key={`${technique.technique_id}-${technique.technique_name}`}
                  className="border-b border-slate-100 text-slate-800"
                >
                  <td className="px-3 py-2 font-mono text-xs">
                    {technique.technique_id}
                  </td>
                  <td className="px-3 py-2">
                    {technique.technique_name}
                  </td>
                  <td className="px-3 py-2">
                    {technique.evidence_count}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
