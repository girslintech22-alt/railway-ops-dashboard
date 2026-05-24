from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

REQUIRED_FIELDS: tuple[str, ...] = (
    "trainNumber",
    "trainName",
    "trainType",
    "sequence",
    "stationCode",
    "stationName",
    "isHalt",
    "scheduledArrival",
    "scheduledDeparture",
    "haltDurationMinutes",
    "distanceFromSourceKm",
    "speedOnSectionKmph",
    "platform",
    "day",
)


def load_snapshot_files(raw_dir: str | Path = "data/raw") -> list[dict[str, Any]]:
    """Load all JSON snapshot files from the raw data directory.

    Args:
        raw_dir: Directory containing raw snapshot JSON files.

    Returns:
        A list of decoded JSON payloads.
    """
    raw_path = Path(raw_dir)
    if not raw_path.exists():
        logger.warning("event=raw_directory_missing path=%s", raw_path)
        return []

    snapshots: list[dict[str, Any]] = []
    for file_path in sorted(raw_path.glob("*.json")):
        try:
            payload = json.loads(file_path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                snapshots.append(payload)
            else:
                logger.warning("event=snapshot_not_object file=%s", file_path)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("event=snapshot_read_failed file=%s error=%s", file_path, exc)
    logger.info("event=snapshots_loaded count=%s", len(snapshots))
    return snapshots


def validate_snapshot_payload(snapshot: dict[str, Any]) -> bool:
    """Validate that a snapshot has the expected route payload shape.

    Args:
        snapshot: Decoded snapshot dictionary.

    Returns:
        True when payload contains expected keys and route list, else False.
    """
    data = snapshot.get("data")
    if not isinstance(data, dict):
        return False
    train = data.get("train")
    route = data.get("route")
    return isinstance(train, dict) and isinstance(route, list)


def normalize_route_stop(stop: dict[str, Any], train_meta: dict[str, Any]) -> dict[str, Any]:
    """Normalize a single route stop into a flat analytics-ready record.

    Args:
        stop: Raw route stop record from snapshot payload.
        train_meta: Raw train metadata from snapshot payload.

    Returns:
        A normalized route stop dictionary with stable keys.
    """
    normalized: dict[str, Any] = {
        "trainNumber": train_meta.get("trainNumber"),
        "trainName": train_meta.get("trainName"),
        "trainType": train_meta.get("type"),
        "sequence": stop.get("sequence"),
        "stationCode": stop.get("stationCode"),
        "stationName": stop.get("stationName"),
        "isHalt": stop.get("isHalt"),
        "scheduledArrival": stop.get("scheduledArrival"),
        "scheduledDeparture": stop.get("scheduledDeparture"),
        "haltDurationMinutes": stop.get("haltDurationMinutes"),
        "distanceFromSourceKm": stop.get("distanceFromSourceKm"),
        "speedOnSectionKmph": stop.get("speedOnSectionKmph"),
        "platform": stop.get("platform"),
        "day": stop.get("day"),
    }

    for key in REQUIRED_FIELDS:
        normalized.setdefault(key, None)

    return normalized


def prevent_duplicate_route_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Remove duplicate route records while preserving order.

    Args:
        records: Normalized route records.

    Returns:
        Deduplicated normalized route records.
    """
    seen: set[tuple[Any, Any, Any, Any]] = set()
    deduped: list[dict[str, Any]] = []

    for record in records:
        key = (
            record.get("trainNumber"),
            record.get("sequence"),
            record.get("stationCode"),
            record.get("day"),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(record)

    if len(deduped) != len(records):
        logger.info("event=duplicates_removed removed=%s", len(records) - len(deduped))

    return deduped


def extract_route_data(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract and normalize all route stop records from one snapshot.

    Args:
        snapshot: Decoded snapshot dictionary.

    Returns:
        A list of normalized route stop records. Returns empty list for malformed payloads.
    """
    if not validate_snapshot_payload(snapshot):
        logger.warning("event=invalid_snapshot_payload")
        return []

    data = snapshot["data"]
    train_meta = data.get("train", {})
    route = data.get("route", [])

    normalized_records = [
        normalize_route_stop(stop, train_meta)
        for stop in route
        if isinstance(stop, dict)
    ]

    deduped_records = prevent_duplicate_route_records(normalized_records)
    logger.info(
        "event=route_extracted train=%s stops=%s deduped=%s",
        train_meta.get("trainNumber"),
        len(normalized_records),
        len(deduped_records),
    )
    return deduped_records


def save_processed_route_data(data: list[dict[str, Any]], output_path: str) -> None:
    """Persist normalized route records to a JSON file.

    Args:
        data: Normalized route records.
        output_path: Target JSON file path.
    """
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("event=processed_route_saved path=%s records=%s", output, len(data))


def process_all_route_snapshots(
    raw_dir: str | Path = "data/raw",
    output_path: str = "data/processed/route_segments.json",
) -> list[dict[str, Any]]:
    """Process all raw snapshot files and save a consolidated normalized route dataset.

    Args:
        raw_dir: Raw snapshot directory path.
        output_path: Processed route output file path.

    Returns:
        Consolidated deduplicated normalized route records.
    """
    snapshots = load_snapshot_files(raw_dir)
    all_records: list[dict[str, Any]] = []

    for snapshot in snapshots:
        all_records.extend(extract_route_data(snapshot))

    all_records = prevent_duplicate_route_records(all_records)
    save_processed_route_data(all_records, output_path)
    return all_records
