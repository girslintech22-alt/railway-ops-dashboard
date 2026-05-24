import type { Corridor } from "../data/mockData";

const severityClass: Record<Corridor["severity"], string> = {
  stable: "text-cyan",
  moderate: "text-amber",
  critical: "text-alert",
};

export function BottleneckPanel({ corridors }: { corridors: Corridor[] }) {
  return (
    <div className="space-y-3">
      {corridors.map((c) => (
        <div key={c.id} className="rounded border border-white/10 bg-black/15 p-2.5">
          <div className="flex items-start justify-between">
            <div>
              <div className="text-sm text-slate-200">{c.label}</div>
              <div className={`text-[10px] font-semibold tracking-[0.14em] ${severityClass[c.severity]}`}>
                {c.state}
              </div>
            </div>
            <div className={`text-[10px] font-semibold uppercase tracking-[0.14em] ${severityClass[c.severity]}`}>
              {c.severity}
            </div>
          </div>
          <div className="mt-2 h-1.5 w-full rounded bg-white/5">
            <div className="h-1.5 rounded bg-amber" style={{ width: `${c.pressure}%` }} />
          </div>
          <div className="mt-2 grid grid-cols-2 gap-y-1 text-[11px] text-muted">
            <div>+{c.delaySpikePct}% delay spike</div>
            <div className="text-right">Recovery ETA: {c.recoveryEtaMin}m</div>
            <div>Throughput impact {100 - c.throughput}%</div>
            <div className="text-right">Flow {c.throughput}%</div>
          </div>
        </div>
      ))}
    </div>
  );
}
