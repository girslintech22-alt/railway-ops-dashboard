"use client";

import { useEffect, useMemo, useState } from "react";
import { baseCorridors, baseHealth, baseNodes, baseRanking, baseSeries, baseTelemetry, type Corridor, type HealthMetric } from "../lib/mockData";

function seeded(index: number, step: number): number {
  const x = Math.sin(index * 12.9898 + step * 78.233) * 43758.5453;
  return x - Math.floor(x);
}

export function useSimulation() {
  const [tick, setTick] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setTick((v) => v + 1), 7000);
    return () => clearInterval(id);
  }, []);

  const state = useMemo(() => {
    const health: HealthMetric[] = baseHealth.map((h, i) => {
      if (h.label === "Avg Delay") return { ...h, value: `${(7.1 + seeded(i, tick) * 1.8).toFixed(1)}m` };
      if (h.label === "On-Time %") return { ...h, value: `${(92.2 + seeded(i, tick) * 2.3).toFixed(1)}%` };
      if (h.label === "Avg Corridor Speed") return { ...h, value: `${(86 + seeded(i, tick) * 4.5).toFixed(1)} km/h` };
      return h;
    });

    const corridors: Corridor[] = baseCorridors.map((c, i) => {
      const drift = Math.round(seeded(i, tick) * 8 - 4);
      const pressure = Math.max(35, Math.min(95, c.pressure + drift));
      const throughput = Math.max(60, Math.min(95, c.throughput - Math.floor(drift / 2)));
      return { ...c, pressure, throughput };
    });

    const nodes = baseNodes.map((n, i) => ({ ...n, load: Math.max(50, Math.min(97, n.load + Math.round(seeded(i, tick) * 10 - 5))) }));
    const series = baseSeries.map((p, i) => ({ ...p, actual: Math.max(84, Math.min(97, p.actual + (seeded(i, tick) - 0.5) * 1.6)) }));
    const telemetry = [`TELEMETRY T+${tick * 7}s | Premium network dispatch update committed`, ...baseTelemetry].slice(0, 7);

    return { health, corridors, nodes, series, ranking: baseRanking, telemetry, tick };
  }, [tick]);

  return state;
}
