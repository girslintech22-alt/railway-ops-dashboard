from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def _to_float(value: Any) -> float | None:
    """Safely convert value to float, returning None for null or invalid inputs."""
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: Any) -> int | None:
    """Safely convert value to int, returning None for null or invalid inputs."""
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _load_json_list(path: str | Path) -> list[dict[str, Any]]:
    """Load a JSON list from disk, returning empty list for malformed or missing files."""
    file_path = Path(path)
    if not file_path.exists():
        logger.warning("event=input_missing path=%s", file_path)
        return []
    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("event=input_read_failed path=%s error=%s", file_path, exc)
        return []
    logger.warning("event=input_not_list path=%s", file_path)
    return []


def _save_json(data: list[dict[str, Any]], path: str | Path) -> None:
    """Write JSON payload to disk with deterministic formatting."""
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _dedupe(records: list[dict[str, Any]], key_fields: tuple[str, ...]) -> list[dict[str, Any]]:
    """Deduplicate records while preserving order using stable key fields."""
    seen: set[tuple[Any, ...]] = set()
    unique: list[dict[str, Any]] = []
    for record in records:
        key = tuple(record.get(field) for field in key_fields)
        if key in seen:
            continue
        seen.add(key)
        unique.append(record)
    return unique


def compute_route_efficiency(train_summary: dict[str, Any]) -> dict[str, Any]:
    """Compute route efficiency metrics for a single train summary."""
    distance_km = _to_float(train_summary.get("distanceKm"))
    total_halts = _to_int(train_summary.get("totalHalts"))
    travel_time_minutes = _to_float(train_summary.get("travelTimeMinutes"))

    avg_kmph = None
    if distance_km is not None and travel_time_minutes and travel_time_minutes > 0:
        avg_kmph = round(distance_km / (travel_time_minutes / 60.0), 2)

    halt_density = None
    if distance_km and distance_km > 0 and total_halts is not None:
        halt_density = round(total_halts / distance_km, 4)

    return {
        "trainNumber": train_summary.get("trainNumber"),
        "trainName": train_summary.get("trainName"),
        "distanceKm": distance_km,
        "totalHalts": total_halts,
        "travelTimeMinutes": travel_time_minutes,
        "computedAvgSpeedKmph": avg_kmph,
        "haltsPerKm": halt_density,
    }


def compute_halt_efficiency(route_segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Compute halt efficiency per station stop from route segments."""
    records: list[dict[str, Any]] = []
    for segment in route_segments:
        halt_duration = _to_float(segment.get("haltDurationMinutes"))
        is_halt = _to_int(segment.get("isHalt"))
        if is_halt != 1:
            continue
        records.append(
            {
                "trainNumber": segment.get("trainNumber"),
                "stationCode": segment.get("stationCode"),
                "stationName": segment.get("stationName"),
                "sequence": _to_int(segment.get("sequence")),
                "day": _to_int(segment.get("day")),
                "haltDurationMinutes": halt_duration,
                "isEfficientHalt": halt_duration is not None and halt_duration <= 5,
            }
        )

    deduped = _dedupe(records, ("trainNumber", "stationCode", "sequence", "day"))
    return sorted(
        deduped,
        key=lambda x: (
            x.get("trainNumber") or "",
            x.get("day") if x.get("day") is not None else 9999,
            x.get("sequence") if x.get("sequence") is not None else 9999,
        ),
    )


def compute_corridor_speed_rankings(route_segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Rank corridor sections by speed using stable deterministic sorting."""
    records: list[dict[str, Any]] = []
    for segment in route_segments:
        speed = _to_float(segment.get("speedOnSectionKmph"))
        if speed is None:
            continue
        records.append(
            {
                "trainNumber": segment.get("trainNumber"),
                "trainName": segment.get("trainName"),
                "sequence": _to_int(segment.get("sequence")),
                "stationCode": segment.get("stationCode"),
                "stationName": segment.get("stationName"),
                "day": _to_int(segment.get("day")),
                "speedOnSectionKmph": speed,
            }
        )

    records = _dedupe(records, ("trainNumber", "sequence", "stationCode", "day"))
    ranked = sorted(
        records,
        key=lambda x: (
            -(x.get("speedOnSectionKmph") or -1.0),
            x.get("trainNumber") or "",
            x.get("day") if x.get("day") is not None else 9999,
            x.get("sequence") if x.get("sequence") is not None else 9999,
        ),
    )

    for idx, item in enumerate(ranked, start=1):
        item["rank"] = idx
    return ranked


def compute_train_rankings(train_summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Rank trains by speed, then fewer halts, then shorter travel time."""
    rows: list[dict[str, Any]] = []
    for summary in train_summaries:
        rows.append(
            {
                "trainNumber": summary.get("trainNumber"),
                "trainName": summary.get("trainName"),
                "trainType": summary.get("trainType"),
                "avgSpeedKmph": _to_float(summary.get("avgSpeedKmph")),
                "totalHalts": _to_int(summary.get("totalHalts")),
                "travelTimeMinutes": _to_float(summary.get("travelTimeMinutes")),
            }
        )

    rows = _dedupe(rows, ("trainNumber",))
    ranked = sorted(
        rows,
        key=lambda x: (
            -(x.get("avgSpeedKmph") if x.get("avgSpeedKmph") is not None else -1.0),
            x.get("totalHalts") if x.get("totalHalts") is not None else 999999,
            x.get("travelTimeMinutes") if x.get("travelTimeMinutes") is not None else 999999.0,
            x.get("trainNumber") or "",
        ),
    )
    for idx, item in enumerate(ranked, start=1):
        item["rank"] = idx
    return ranked


def generate_kpi_report(
    train_summaries_path: str | Path = "data/processed/train_summaries.json",
    route_segments_path: str | Path = "data/processed/route_segments.json",
    output_dir: str | Path = "data/analytics",
) -> dict[str, Any]:
    """Generate and save all KPI datasets from processed local inputs."""
    train_summaries = _load_json_list(train_summaries_path)
    route_segments = _load_json_list(route_segments_path)

    route_efficiency = [compute_route_efficiency(item) for item in train_summaries]
    route_efficiency = _dedupe(route_efficiency, ("trainNumber",))
    route_efficiency = sorted(route_efficiency, key=lambda x: x.get("trainNumber") or "")

    halt_efficiency = compute_halt_efficiency(route_segments)
    corridor_rankings = compute_corridor_speed_rankings(route_segments)
    train_rankings = compute_train_rankings(train_summaries)

    output_base = Path(output_dir)
    _save_json(route_efficiency, output_base / "route_efficiency.json")
    _save_json(halt_efficiency, output_base / "halt_efficiency.json")
    _save_json(corridor_rankings, output_base / "corridor_rankings.json")
    _save_json(train_rankings, output_base / "train_rankings.json")

    report = {
        "routeEfficiencyCount": len(route_efficiency),
        "haltEfficiencyCount": len(halt_efficiency),
        "corridorRankingsCount": len(corridor_rankings),
        "trainRankingsCount": len(train_rankings),
        "outputDir": str(output_base),
    }
    logger.info("event=kpi_report_generated %s", report)
    return report
