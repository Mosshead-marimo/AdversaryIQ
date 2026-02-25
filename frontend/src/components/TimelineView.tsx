import type { ExecutionTimelineEvent } from "@/types/report";

interface TimelineViewProps {
  events: ExecutionTimelineEvent[];
}

const sortByTimestamp = (events: ExecutionTimelineEvent[]) =>
  [...events].sort((a, b) => {
    const aTs = a.timestamp ? Date.parse(a.timestamp) : 0;
    const bTs = b.timestamp ? Date.parse(b.timestamp) : 0;
    return aTs - bTs;
  });

export default function TimelineView({ events }: TimelineViewProps) {
  const sortedEvents = sortByTimestamp(events);

  return (
    <section className="rounded-2xl bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold text-slate-900">
        Execution Timeline
      </h2>

      <div className="max-h-[26rem] space-y-2 overflow-y-auto pr-1">
        {sortedEvents.length === 0 && (
          <p className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-500">
            No execution timeline events returned.
          </p>
        )}

        {sortedEvents.map((event, index) => (
          <article
            key={`${event.timestamp || "event"}-${index}`}
            className="rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm"
          >
            <div className="flex flex-wrap items-center gap-2 text-slate-700">
              {event.pid !== undefined && (
                <span className="rounded bg-slate-900 px-2 py-0.5 font-mono text-xs text-slate-50">
                  PID {event.pid}
                </span>
              )}
              {event.type && (
                <span className="font-semibold text-slate-900">
                  {event.type}
                </span>
              )}
              {event.target && (
                <span className="truncate text-slate-600">
                  {"->"} {event.target}
                </span>
              )}
            </div>
            {event.timestamp && (
              <p className="mt-1 font-mono text-xs text-slate-500">
                {event.timestamp}
              </p>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}
