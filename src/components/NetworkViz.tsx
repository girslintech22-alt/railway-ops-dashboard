import type { Corridor } from "../data/mockData";

type Node = { name: string; x: number; y: number; load: number };

const toneBySeverity: Record<Corridor["severity"], string> = {
  stable: "#62c5d7",
  moderate: "#f2b84b",
  critical: "#e45d5d",
};

export function NetworkViz({ nodes, corridors }: { nodes: Node[]; corridors: Corridor[] }) {
  const links = [
    { from: [16, 22], to: [22, 75], id: "NDLS-MMCT" },
    { from: [16, 22], to: [80, 30], id: "NDLS-HWH" },
    { from: [16, 22], to: [76, 79], id: "NDLS-MAS" },
    { from: [22, 75], to: [35, 62], id: "BCT-ADI" },
  ];

  return (
    <div className="relative h-[250px] w-full overflow-hidden rounded-md border border-white/10 bg-[#121821]">
      <svg viewBox="0 0 100 100" className="absolute inset-0 h-full w-full">
        <defs>
          <pattern id="rail-grid" width="8" height="8" patternUnits="userSpaceOnUse">
            <path d="M 8 0 L 0 0 0 8" fill="none" stroke="#1d2631" strokeWidth="0.4" />
          </pattern>
        </defs>
        <rect width="100" height="100" fill="url(#rail-grid)" />
        {links.map((link) => {
          const c = corridors.find((x) => x.id === link.id);
          const color = c ? toneBySeverity[c.severity] : "#62c5d7";
          const thickness = c ? 1 + c.pressure / 40 : 2;
          return <line key={link.id} x1={link.from[0]} y1={link.from[1]} x2={link.to[0]} y2={link.to[1]} stroke={color} strokeOpacity={0.7} strokeWidth={thickness} />;
        })}
        {nodes.map((n) => (
          <g key={n.name}>
            <circle cx={n.x} cy={n.y} r="2.4" fill={n.load > 85 ? "#e45d5d" : n.load > 70 ? "#f2b84b" : "#62c5d7"} opacity={0.55 + n.load / 220} />
            <text x={n.x + 2} y={n.y - 2} fill="#a5b2c4" fontSize="3">{n.name}</text>
          </g>
        ))}
      </svg>
      <div className="telemetry-scan absolute inset-x-0 top-0 h-12 animate-pulse" />
    </div>
  );
}
