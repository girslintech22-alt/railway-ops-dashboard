import { Line, LineChart, ReferenceArea, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

type Point = { t: string; actual: number; expected: number };
type EventPoint = { t: string; note: string };

export function HeroInsightChart({ data, events }: { data: Point[]; events: EventPoint[] }) {
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer>
        <LineChart data={data} margin={{ top: 12, right: 16, left: -26, bottom: 0 }}>
          <ReferenceArea x1="11:00" x2="13:00" fill="#f2b84b" fillOpacity={0.08} />
          <XAxis dataKey="t" tick={{ fill: "#94A0AF", fontSize: 11 }} axisLine={false} tickLine={false} />
          <YAxis domain={[82, 98]} tick={{ fill: "#94A0AF", fontSize: 11 }} axisLine={false} tickLine={false} />
          <Tooltip contentStyle={{ background: "#171d24", border: "1px solid #2d3440", color: "#e8edf4" }} />
          <Line type="monotone" dataKey="expected" stroke="#606b79" strokeDasharray="4 4" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="actual" stroke="#62c5d7" strokeWidth={3} dot={false} />
          {events.map((e) => (
            <ReferenceLine key={e.t} x={e.t} stroke="#f2b84b" strokeOpacity={0.45} strokeDasharray="2 4" />
          ))}
        </LineChart>
      </ResponsiveContainer>
      <div className="mt-2 grid grid-cols-3 gap-2 text-[11px] text-muted">
        {events.map((e) => (
          <div key={e.t} className="rounded border border-white/10 px-2 py-1">
            <span className="text-amber">{e.t}</span> {e.note}
          </div>
        ))}
      </div>
    </div>
  );
}
