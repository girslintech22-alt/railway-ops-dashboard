import json
from pathlib import Path

from processing.train_processor import (
    extract_train_summary,
    process_all_train_snapshots,
    save_train_summaries,
)


def load_sample_snapshot() -> dict:
    return json.loads(Path("data/raw/sample1.json").read_text(encoding="utf-8"))


def test_valid_extraction() -> None:
    summary = extract_train_summary(load_sample_snapshot())
    assert summary["trainNumber"] == "12951"
    assert summary["trainName"] == "New Delhi Tejas Rajdhani Express"
    assert summary["trainType"] == "Rajdhani Express"
    assert isinstance(summary["runningDays"], list)


def test_malformed_payloads() -> None:
    malformed = {"data": {"route": []}}
    assert extract_train_summary(malformed) == {}


def test_missing_optional_fields() -> None:
    snapshot = {
        "data": {
            "train": {
                "trainNumber": "10001",
                "trainName": "Mini",
                "type": "Express",
            }
        }
    }
    summary = extract_train_summary(snapshot)
    assert summary["sourceStationCode"] is None
    assert summary["runningDays"] is None
    assert summary["runningAllDays"] is None


def test_duplicate_prevention(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    sample = load_sample_snapshot()
    (raw_dir / "a.json").write_text(json.dumps(sample), encoding="utf-8")
    (raw_dir / "b.json").write_text(json.dumps(sample), encoding="utf-8")

    current = Path.cwd()
    try:
        # keep output generation compatible with processor defaults
        import os

        os.chdir(tmp_path)
        records = process_all_train_snapshots(raw_dir=raw_dir)
    finally:
        os.chdir(current)

    assert len(records) == 1


def test_processed_file_generation(tmp_path: Path) -> None:
    output_file = tmp_path / "train_summaries.json"
    summary = extract_train_summary(load_sample_snapshot())

    save_train_summaries([summary], str(output_file))
    assert output_file.exists()
    loaded = json.loads(output_file.read_text(encoding="utf-8"))
    assert isinstance(loaded, list)
    assert loaded[0]["trainNumber"] == "12951"
