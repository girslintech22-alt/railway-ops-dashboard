export function TelemetryFeed({ rows }: { rows: string[] }) {
  return (
    <div className="h-[180px] overflow-hidden rounded-md border border-white/10 bg-[#121821] p-3">
      <div className="mb-2 text-[10px] uppercase tracking-[0.18em] text-muted">Live Operations Feed</div>
      <div className="space-y-1 font-mono text-[11px] text-slate-300">
        {rows.map((r, i) => (
          <div key={r + i} className="border-b border-white/5 pb-1">&gt; {r}</div>
        ))}
      </div>
    </div>
  );
}
