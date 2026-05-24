"use client";

import { motion } from "framer-motion";
import { CartesianGrid, Line, LineChart, ReferenceArea, ResponsiveContainer, Tooltip, XAxis, YAxis, BarChart, Bar } from "recharts";
import { baseCorridors, eventMarkers } from "../lib/mockData";
import { useSimulation } from "../lib/useSimulation";

function toneClass(tone: string) {
  if (tone === "alert") return "bg-alert";
  if (tone === "warn") return "bg-amber";
  return "bg-cyan";
}

export default function Page() {
  const now = new Date().toLocaleString();
  const { health, corridors, nodes, series, ranking, telemetry } = useSimulation();

  return (
    <main className="track-grid h-screen overflow-hidden bg-graphite px-5 py-4 text-slate-100">
      <div className="mx-auto grid h-full max-w-[1880px] grid-rows-[auto_auto_1fr] gap-4">
        <header className="grid grid-cols-[1.35fr_1fr] items-end gap-4 border-b border-white/10 pb-2">
          <div>
            <h1 className="text-3xl font-semibold tracking-tight">Premium Railway Operational Intelligence</h1>
            <p className="mt-1 text-sm text-muted">Rajdhani corridors maintained 94% punctuality despite peak junction congestion.</p>
            <div className="mt-2 flex items-center gap-3 text-xs text-slate-500">
              <span>Live timestamp: {now}</span>
              <span className="rounded border border-white/15 bg-white/5 px-2 py-0.5 tracking-[0.08em] text-cyan">SIMULATED NETWORK SNAPSHOT</span>
            </div>
          </div>
          <div className="text-right text-xs text-slate-400">Dispatch State: <span className="text-cyan">RECOVERING</span> | Network Resilience: <span className="text-amber">MONITOR</span></div>
        </header>

        <section className="grid grid-cols-8 gap-2 border-b border-white/10 pb-2">
          {health.map((m) => (
            <div key={m.label} className="flex items-center gap-2 border-r border-white/10 pr-2 last:border-r-0">
              <span className={`h-1.5 w-1.5 rounded-full ${toneClass(m.tone)}`} />
              <div>
                <div className="text-[10px] text-muted">{m.label}</div>
                <div className="text-sm font-medium text-slate-200">{m.value}</div>
              </div>
            </div>
          ))}
        </section>

        <section className="grid grid-cols-[1.55fr_1fr_0.95fr] gap-4 overflow-hidden">
          <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="flex h-full flex-col border border-white/10 bg-steel/70 p-4">
            <div className="mb-1 text-xs tracking-[0.12em] text-muted">Main Operational Story</div>
            <h2 className="text-lg">Dispatch intervention reduced delay propagation on premium corridors</h2>
            <p className="mb-2 text-xs text-muted">Expected vs actual recovery after platform reassignment and midday routing intervention.</p>
            <div className="h-[310px] w-full">
              <ResponsiveContainer>
                <LineChart data={series} margin={{ top: 12, right: 16, left: -26, bottom: 0 }}>
                  <ReferenceArea x1="11:00" x2="13:00" fill="#f2b84b" fillOpacity={0.08} />
                  <CartesianGrid stroke="#232d38" strokeOpacity={0.35} vertical={false} />
                  <XAxis dataKey="t" tick={{ fill: "#94A0AF", fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis domain={[82, 98]} tick={{ fill: "#94A0AF", fontSize: 11 }} axisLine={false} tickLine={false} />
                  <Tooltip contentStyle={{ background: "#171d24", border: "1px solid #2d3440", color: "#e8edf4" }} />
                  <Line type="monotone" dataKey="expected" stroke="#606b79" strokeDasharray="4 4" strokeWidth={2} dot={false} />
                  <Line type="monotone" dataKey="actual" stroke="#62c5d7" strokeWidth={3} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-2 grid grid-cols-3 gap-2 text-[11px] text-muted">
              {eventMarkers.map((e) => (
                <div key={e.t} className="rounded border border-white/10 px-2 py-1"><span className="text-amber">{e.t}</span> {e.note}</div>
              ))}
            </div>
          </motion.div>

          <div className="grid h-full grid-rows-[1fr_auto] gap-4">
            <div className="border border-white/10 bg-steel/65 p-3">
              <div className="mb-2 text-xs tracking-[0.12em] text-muted">Live Passenger Network State</div>
              <div className="relative h-[250px] overflow-hidden rounded border border-white/10 bg-[#121821]">
                <svg viewBox="0 0 100 100" className="absolute inset-0 h-full w-full">
                  {baseCorridors.map((c, i) => {
                    const links = [[16, 22, 22, 75], [16, 22, 80, 30], [16, 22, 76, 79], [22, 75, 35, 62]] as const;
                    const l = links[i];
                    const color = c.severity === "critical" ? "#e45d5d" : c.severity === "moderate" ? "#f2b84b" : "#62c5d7";
                    return <line key={c.id} x1={l[0]} y1={l[1]} x2={l[2]} y2={l[3]} stroke={color} strokeWidth={1 + c.pressure / 40} strokeOpacity={0.72} />;
                  })}
                  {nodes.map((n) => (
                    <g key={n.name}><circle cx={n.x} cy={n.y} r="2.4" fill={n.load > 85 ? "#e45d5d" : n.load > 70 ? "#f2b84b" : "#62c5d7"} opacity={0.55 + n.load / 220} /><text x={n.x + 2} y={n.y - 2} fill="#a5b2c4" fontSize="3">{n.name}</text></g>
                  ))}
                </svg>
              </div>
            </div>
            <div className="border border-white/10 bg-steel/65 p-3">
              <div className="mb-1 text-xs tracking-[0.12em] text-muted">Premium Reliability Ranking</div>
              <div className="h-[210px]">
                <ResponsiveContainer>
                  <BarChart data={ranking} layout="vertical" margin={{ left: 10, right: 8 }}>
                    <XAxis type="number" hide />
                    <YAxis dataKey="name" type="category" tick={{ fill: "#9aa4b2", fontSize: 11 }} width={140} />
                    <Bar dataKey="score" fill="#5b6471" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          <div className="grid h-full grid-rows-[1fr_auto] gap-4">
            <div className="border border-white/10 bg-steel/65 p-3">
              <div className="mb-2 text-xs tracking-[0.12em] text-muted">Bottleneck Alert Stack</div>
              <div className="space-y-3">
                {corridors.map((c) => (
                  <div key={c.id} className="rounded border border-white/10 bg-black/15 p-2.5">
                    <div className="flex items-start justify-between"><div><div className="text-sm text-slate-200">{c.label}</div><div className="text-[10px] tracking-[0.14em] text-muted">{c.state}</div></div><div className="text-[10px] uppercase tracking-[0.14em]">{c.severity}</div></div>
                    <div className="mt-2 h-1.5 w-full rounded bg-white/5"><div className="h-1.5 rounded bg-amber" style={{ width: `${c.pressure}%` }} /></div>
                    <div className="mt-2 grid grid-cols-2 gap-y-1 text-[11px] text-muted"><div>+{c.delaySpikePct}% delay spike</div><div className="text-right">Recovery ETA: {c.recoveryEtaMin}m</div><div>Throughput impact {100 - c.throughput}%</div><div className="text-right">Flow {c.throughput}%</div></div>
                  </div>
                ))}
              </div>
            </div>
            <div className="h-[180px] overflow-hidden border border-white/10 bg-[#121821] p-3">
              <div className="mb-2 text-[10px] uppercase tracking-[0.18em] text-muted">Live Operations Feed</div>
              <div className="space-y-1 font-mono text-[11px] text-slate-300">{telemetry.map((r, i) => <div key={r + i} className="border-b border-white/5 pb-1">&gt; {r}</div>)}</div>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
