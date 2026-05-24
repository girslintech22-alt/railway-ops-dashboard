import json
from pathlib import Path

from analytics.kpi_engine import (
    compute_corridor_speed_rankings,
    compute_train_rankings,
    generate_kpi_report,
)


def test_kpi_generation(tmp_path: Path) -> None:
    train_data = [
        {
            "trainNumber": "100",
            "trainName": "A",
            "trainType": "Rajdhani",
            "distanceKm": 1000,
            "totalHalts": 10,
            "travelTimeMinutes": 600,
            "avgSpeedKmph": 95,
        }
    ]
    route_data = [
        {
            "trainNumber": "100",
            "trainName": "A",
            "sequence": 1,
            "stationCode": "AAA",
            "stationName": "Alpha",
            "isHalt": 1,
            "haltDurationMinutes": 3,
            "speedOnSectionKmph": 80,
            "day": 1,
        }
    ]

    train_path = tmp_path / "train_summaries.json"
    route_path = tmp_path / "route_segments.json"
    train_path.write_text(json.dumps(train_data), encoding="utf-8")
    route_path.write_text(json.dumps(route_data), encoding="utf-8")

    report = generate_kpi_report(train_path, route_path, tmp_path / "analytics")
    assert report["trainRankingsCount"] == 1
    assert (tmp_path / "analytics" / "train_rankings.json").exists()


def test_malformed_input_handling(tmp_path: Path) -> None:
    train_path = tmp_path / "train_summaries.json"
    route_path = tmp_path / "route_segments.json"
    train_path.write_text("{bad json", encoding="utf-8")
    route_path.write_text("[]", encoding="utf-8")

    report = generate_kpi_report(train_path, route_path, tmp_path / "analytics")
    assert report["routeEfficiencyCount"] == 0
    assert report["trainRankingsCount"] == 0


def test_empty_dataset_handling(tmp_path: Path) -> None:
    train_path = tmp_path / "train_summaries.json"
    route_path = tmp_path / "route_segments.json"
    train_path.write_text("[]", encoding="utf-8")
    route_path.write_text("[]", encoding="utf-8")

    report = generate_kpi_report(train_path, route_path, tmp_path / "analytics")
    assert report["corridorRankingsCount"] == 0
    assert report["haltEfficiencyCount"] == 0


def test_ranking_stability() -> None:
    trains = [
        {"trainNumber": "B", "trainName": "B", "avgSpeedKmph": 90, "totalHalts": 5, "travelTimeMinutes": 500},
        {"trainNumber": "A", "trainName": "A", "avgSpeedKmph": 90, "totalHalts": 5, "travelTimeMinutes": 500},
    ]
    ranked = compute_train_rankings(trains)
    assert ranked[0]["trainNumber"] == "A"
    assert ranked[1]["trainNumber"] == "B"

    route = [
        {"trainNumber": "B", "sequence": 2, "stationCode": "BBB", "day": 1, "speedOnSectionKmph": 100},
        {"trainNumber": "A", "sequence": 1, "stationCode": "AAA", "day": 1, "speedOnSectionKmph": 100},
    ]
    corridor = compute_corridor_speed_rankings(route)
    assert corridor[0]["trainNumber"] == "A"


def test_output_generation(tmp_path: Path) -> None:
    train_path = tmp_path / "train_summaries.json"
    route_path = tmp_path / "route_segments.json"
    train_path.write_text("[]", encoding="utf-8")
    route_path.write_text("[]", encoding="utf-8")

    generate_kpi_report(train_path, route_path, tmp_path / "analytics")
    assert (tmp_path / "analytics" / "route_efficiency.json").exists()
    assert (tmp_path / "analytics" / "halt_efficiency.json").exists()
    assert (tmp_path / "analytics" / "corridor_rankings.json").exists()
    assert (tmp_path / "analytics" / "train_rankings.json").exists()
