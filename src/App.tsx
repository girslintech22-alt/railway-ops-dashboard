import { motion } from "framer-motion";
import { BottleneckPanel } from "./components/BottleneckPanel";
import { HeroInsightChart } from "./components/HeroInsightChart";
import { NetworkViz } from "./components/NetworkViz";
import { TelemetryFeed } from "./components/TelemetryFeed";
import { TrainRankingChart } from "./components/TrainRankingChart";
import { corridors, healthStrip, heroSeries, networkNodes, operationalEvents, telemetryFeed, trainRanking } from "./data/mockData";

function App() {
  const now = new Date().toLocaleString();

  return (
    <main className="h-screen overflow-hidden bg-graphite px-5 py-4 text-slate-100">
      <div className="mx-auto grid h-full max-w-[1860px] grid-rows-[auto_auto_1fr] gap-4">
        <header className="grid grid-cols-[1.35fr_1fr] items-end gap-4 border-b border-white/10 pb-2">
          <div>
            <h1 className="text-3xl font-semibold tracking-tight">Premium Railway Operational Intelligence</h1>
            <p className="mt-1 text-sm text-muted">Rajdhani corridors maintained 94% punctuality despite peak junction congestion.</p>
            <p className="mt-2 text-xs text-slate-500">Live timestamp: {now}</p>
          </div>
          <div className="text-right text-xs text-slate-400">Dispatch State: <span className="text-cyan">RECOVERING</span> | Network Resilience: <span className="text-amber">MONITOR</span></div>
        </header>

        <section className="grid grid-cols-8 gap-2 border-b border-white/10 pb-2">
          {healthStrip.map((m) => (
            <div key={m.label} className="flex items-center gap-2 border-r border-white/10 pr-2 last:border-r-0">
              <span className={`h-1.5 w-1.5 rounded-full ${m.tone === "alert" ? "bg-alert" : m.tone === "warn" ? "bg-amber" : "bg-cyan"}`} />
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
            <HeroInsightChart data={heroSeries} events={operationalEvents} />
          </motion.div>

          <div className="grid h-full grid-rows-[1fr_auto] gap-4">
            <div className="border border-white/10 bg-steel/65 p-3">
              <div className="mb-2 text-xs tracking-[0.12em] text-muted">Live Passenger Network State</div>
              <NetworkViz nodes={networkNodes} corridors={corridors} />
            </div>
            <div className="border border-white/10 bg-steel/65 p-3">
              <div className="mb-1 text-xs tracking-[0.12em] text-muted">Premium Reliability Ranking</div>
              <TrainRankingChart data={trainRanking} />
            </div>
          </div>

          <div className="grid h-full grid-rows-[1fr_auto] gap-4">
            <div className="border border-white/10 bg-steel/65 p-3">
              <div className="mb-2 text-xs tracking-[0.12em] text-muted">Bottleneck Alert Stack</div>
              <BottleneckPanel corridors={corridors} />
            </div>
            <TelemetryFeed rows={telemetryFeed} />
          </div>
        </section>
      </div>
    </main>
  );
}

export default App;
