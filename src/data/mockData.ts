export type Corridor = {
  id: string;
  label: string;
  pressure: number;
  throughput: number;
  severity: "stable" | "moderate" | "critical";
  delaySpikePct: number;
  recoveryEtaMin: number;
  state: "SIGNAL CLEAR" | "RECOVERING" | "HOLDING" | "SATURATED";
};

export const healthStrip = [
  { label: "Avg Delay", value: "7.8m", tone: "warn" },
  { label: "On-Time %", value: "93.6%", tone: "normal" },
  { label: "Congested Junctions", value: "4", tone: "alert" },
  { label: "Recovery Rate", value: "+11.2%", tone: "normal" },
  { label: "Active Premium Trains", value: "15", tone: "normal" },
  { label: "Propagation Risk", value: "Moderate", tone: "warn" },
  { label: "Avg Corridor Speed", value: "88.4 km/h", tone: "normal" },
  { label: "Dispatch Efficiency", value: "91.3%", tone: "normal" },
] as const;

export const heroSeries = [
  { t: "08:00", actual: 95, expected: 94 },
  { t: "09:00", actual: 93, expected: 93 },
  { t: "10:00", actual: 91, expected: 92 },
  { t: "11:00", actual: 88, expected: 90 },
  { t: "12:00", actual: 86, expected: 88 },
  { t: "13:00", actual: 87, expected: 87 },
  { t: "14:00", actual: 90, expected: 87 },
  { t: "15:00", actual: 92, expected: 88 },
  { t: "16:00", actual: 94, expected: 89 },
];

export const operationalEvents = [
  { t: "11:40", note: "Platform reassignment initiated" },
  { t: "12:10", note: "NDLS congestion peaked" },
  { t: "13:05", note: "Rajdhani recovery acceleration detected" },
];

export const corridors: Corridor[] = [
  { id: "NDLS-MMCT", label: "NDLS ↔ MMCT", pressure: 86, throughput: 71, severity: "critical", delaySpikePct: 18, recoveryEtaMin: 42, state: "SATURATED" },
  { id: "NDLS-HWH", label: "NDLS ↔ HWH", pressure: 72, throughput: 78, severity: "moderate", delaySpikePct: 9, recoveryEtaMin: 26, state: "RECOVERING" },
  { id: "NDLS-MAS", label: "NDLS ↔ MAS", pressure: 64, throughput: 82, severity: "moderate", delaySpikePct: 6, recoveryEtaMin: 18, state: "HOLDING" },
  { id: "BCT-ADI", label: "BCT ↔ ADI", pressure: 43, throughput: 89, severity: "stable", delaySpikePct: 2, recoveryEtaMin: 8, state: "SIGNAL CLEAR" },
];

export const trainRanking = [
  { name: "Vande Bharat 22436", score: 96 },
  { name: "Rajdhani 12951", score: 94 },
  { name: "Shatabdi 12009", score: 91 },
  { name: "Duronto 12213", score: 89 },
  { name: "Rajdhani 12301", score: 88 },
];

export const networkNodes = [
  { name: "NDLS", x: 16, y: 22, load: 92 },
  { name: "MMCT", x: 22, y: 75, load: 81 },
  { name: "HWH", x: 80, y: 30, load: 74 },
  { name: "MAS", x: 76, y: 79, load: 67 },
  { name: "ADI", x: 35, y: 62, load: 58 },
  { name: "KOTA", x: 38, y: 43, load: 84 },
];

export const telemetryFeed = [
  "SIGNAL CLEAR | 22436 held 95% punctuality post Kanpur",
  "RECOVERING | NDLS-MMCT delay wave contained after 13:10",
  "PLATFORM SHIFT | NDLS platform allocation rebalanced for Rajdhani cluster",
  "SATURATED | MMCT junction wait crossed threshold for 9 minutes",
  "ROUTE NORMALIZED | BCT-ADI corridor variance returned to baseline",
  "DISPATCH NOTE | Premium network resilience index improved 4.2 points",
];
