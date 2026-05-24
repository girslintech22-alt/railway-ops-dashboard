from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

TRAIN_SUMMARY_FIELDS: tuple[str, ...] = (
    "trainNumber",
    "trainName",
    "trainType",
    "sourceStationCode",
    "sourceStationName",
    "destinationStationCode",
    "destinationStationName",
    "totalHalts",
    "distanceKm",
    "avgSpeedKmph",
    "travelTimeMinutes",
    "runningDays",
    "runningAllDays",
    "returnTrainNumber",
)


def load_snapshot_files(raw_dir: str | Path = "data/raw") -> list[dict[str, Any]]:
    """Load all local raw JSON snapshot payloads.

    Args:
        raw_dir: Directory containing raw snapshot JSON files.

    Returns:
        List of decoded snapshot dictionaries.
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

    logger.info("event=train_snapshots_loaded count=%s", len(snapshots))
    return snapshots


def validate_train_payload(snapshot: dict[str, Any]) -> bool:
    """Validate that snapshot contains train metadata payload.

    Args:
        snapshot: Snapshot dictionary decoded from JSON.

    Returns:
        True when train metadata exists in expected structure.
    """
    data = snapshot.get("data")
    if not isinstance(data, dict):
        return False
    train = data.get("train")
    return isinstance(train, dict)


def extract_train_summary(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Extract one normalized train summary from a snapshot.

    Args:
        snapshot: Snapshot dictionary decoded from JSON.

    Returns:
        Flat normalized train summary dictionary. Returns empty dict for malformed payloads.
    """
    if not validate_train_payload(snapshot):
        logger.warning("event=invalid_train_payload")
        return {}

    train = snapshot["data"].get("train", {})
    running_days = train.get("runningDays") if isinstance(train.get("runningDays"), dict) else {}

    summary: dict[str, Any] = {
        "trainNumber": train.get("trainNumber"),
        "trainName": train.get("trainName"),
        "trainType": train.get("type"),
        "sourceStationCode": train.get("sourceStationCode"),
        "sourceStationName": train.get("sourceStationName"),
        "destinationStationCode": train.get("destinationStationCode"),
        "destinationStationName": train.get("destinationStationName"),
        "totalHalts": train.get("totalHalts"),
        "distanceKm": train.get("distanceKm"),
        "avgSpeedKmph": train.get("avgSpeedKmph"),
        "travelTimeMinutes": train.get("travelTimeMinutes"),
        "runningDays": running_days.get("days"),
        "runningAllDays": running_days.get("allDays"),
        "returnTrainNumber": train.get("returnTrainNumber"),
    }

    for key in TRAIN_SUMMARY_FIELDS:
        summary.setdefault(key, None)

    return summary


def prevent_duplicate_train_summaries(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Remove duplicate train summaries while preserving order.

    Args:
        data: Normalized train summary records.

    Returns:
        Deduplicated train summary records.
    """
    seen: set[tuple[Any, Any]] = set()
    deduped: list[dict[str, Any]] = []

    for item in data:
        key = (item.get("trainNumber"), item.get("returnTrainNumber"))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    if len(deduped) != len(data):
        logger.info("event=train_duplicates_removed removed=%s", len(data) - len(deduped))

    return deduped


def save_train_summaries(data: list[dict[str, Any]], output_path: str) -> None:
    """Save normalized train summaries to disk.

    Args:
        data: Normalized train summary records.
        output_path: Destination JSON path.
    """
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("event=train_summaries_saved path=%s records=%s", output, len(data))


def process_all_train_snapshots(raw_dir: str | Path = "data/raw") -> list[dict[str, Any]]:
    """Process all local snapshots into normalized deduplicated train summaries.

    Args:
        raw_dir: Directory containing raw snapshot JSON files.

    Returns:
        Deduplicated list of normalized train summary dictionaries.
    """
    snapshots = load_snapshot_files(raw_dir)
    summaries: list[dict[str, Any]] = []

    for snapshot in snapshots:
        summary = extract_train_summary(snapshot)
        if summary:
            summaries.append(summary)

    summaries = prevent_duplicate_train_summaries(summaries)
    save_train_summaries(summaries, "data/processed/train_summaries.json")
    logger.info("event=train_processing_complete records=%s", len(summaries))
    return summaries
