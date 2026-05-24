import { motion } from "framer-motion";

type IndicatorProps = { label: string; value: string; tone?: "normal" | "warn" | "alert" };

export function IndicatorPill({ label, value, tone = "normal" }: IndicatorProps) {
  const toneClass = tone === "alert" ? "text-alert" : tone === "warn" ? "text-amber" : "text-cyan";

  return (
    <motion.div
      initial={{ opacity: 0, y: -4 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex items-center gap-2 rounded-md border border-white/10 bg-steel/70 px-3 py-2"
    >
      <span className={`h-2 w-2 rounded-full ${toneClass} bg-current`} />
      <div className="text-[10px] uppercase tracking-[0.12em] text-muted">{label}</div>
      <div className={`text-xs font-semibold ${toneClass}`}>{value}</div>
    </motion.div>
  );
}
