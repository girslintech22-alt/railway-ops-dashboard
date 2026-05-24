import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from "recharts";

export function TrainRankingChart({ data }: { data: { name: string; score: number }[] }) {
  const withColor = data.map((d, idx) => ({ ...d, fill: idx === 0 ? "#62c5d7" : "#5b6471" }));
  return (
    <div className="h-[220px] w-full">
      <ResponsiveContainer>
        <BarChart data={withColor} layout="vertical" margin={{ left: 12, right: 8 }}>
          <XAxis type="number" hide />
          <YAxis dataKey="name" type="category" tick={{ fill: "#9aa4b2", fontSize: 11 }} width={140} />
          <Bar dataKey="score" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
