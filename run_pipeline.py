from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from analytics.kpi_engine import generate_kpi_report
from config.trains import PREMIUM_TRAINS
from ingestion.poller import fetch_train_data, get_api_key, get_headers, save_raw_response, setup_logging
from processing.route_processor import process_all_route_snapshots
from processing.train_processor import process_all_train_snapshots


ANALYTICS_FILES: tuple[str, ...] = (
    "route_efficiency.json",
    "halt_efficiency.json",
    "corridor_rankings.json",
    "train_rankings.json",
)


def _load_json_list(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"Expected JSON list in {path}")
    return [row for row in payload if isinstance(row, dict)]


def run_one_time_pipeline() -> dict[str, Any]:
    """Run one-time end-to-end ingestion, processing, analytics, and dataset validation."""
    setup_logging()
    logging.info("stage=ingestion status=started")

    api_key = get_api_key()
    headers = get_headers(api_key)

    attempted = 0
    success = 0
    failed = 0
    raw_files: list[str] = []

    for train in PREMIUM_TRAINS:
        train_number = str(train.get("train_no", "")).strip()
        if not train_number:
            continue

        attempted += 1
        payload = fetch_train_data(train_number, headers)
        if payload is None:
            failed += 1
            logging.error("event=ingestion_failed train=%s", train_number)
            continue

        out_path = save_raw_response(train_number, payload)
        raw_files.append(str(out_path))
        success += 1
        logging.info("event=ingestion_success train=%s file=%s", train_number, out_path)

    logging.info("stage=ingestion status=completed attempted=%s success=%s failed=%s", attempted, success, failed)

    logging.info("stage=processing status=started")
    train_summaries = process_all_train_snapshots()
    route_segments = process_all_route_snapshots()
    logging.info(
        "stage=processing status=completed train_summaries=%s route_segments=%s",
        len(train_summaries),
        len(route_segments),
    )

    logging.info("stage=analytics status=started")
    kpi_report = generate_kpi_report()
    logging.info("stage=analytics status=completed report=%s", kpi_report)

    logging.info("stage=dashboard_dataset_validation status=started")
    analytics_dir = Path("data/analytics")
    generated_counts: dict[str, int] = {}
    malformed_files: list[str] = []

    for filename in ANALYTICS_FILES:
        target = analytics_dir / filename
        try:
            rows = _load_json_list(target)
            generated_counts[filename] = len(rows)
        except Exception:
            malformed_files.append(str(target))

    rankings_valid = generated_counts.get("train_rankings.json", 0) > 0 and generated_counts.get("corridor_rankings.json", 0) > 0
    logging.info(
        "stage=dashboard_dataset_validation status=completed rankings_valid=%s malformed_files=%s",
        rankings_valid,
        len(malformed_files),
    )

    summary = {
        "trains_attempted": attempted,
        "successful_polls": success,
        "failed_polls": failed,
        "snapshots_generated": len(raw_files),
        "analytics_files_generated": len(generated_counts),
        "analytics_record_counts": generated_counts,
        "malformed_output_files": malformed_files,
        "dashboard_rankings_valid": rankings_valid,
        "kpi_report": kpi_report,
    }
    logging.info("stage=pipeline status=completed summary=%s", summary)
    return summary


if __name__ == "__main__":
    result = run_one_time_pipeline()
    print(json.dumps(result, indent=2))
