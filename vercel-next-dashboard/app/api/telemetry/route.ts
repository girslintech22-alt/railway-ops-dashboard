import { NextResponse } from "next/server";
import { baseTelemetry } from "../../../lib/mockData";

export async function GET() {
  const now = new Date().toISOString();
  return NextResponse.json({
    timestamp: now,
    feed: [
      `SNAPSHOT ${now} | Premium corridor telemetry refreshed`,
      ...baseTelemetry,
    ],
  });
}
