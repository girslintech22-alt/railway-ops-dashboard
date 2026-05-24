from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

ACCENT = "#4FB3C8"
BG = "#0F1115"
CARD = "#171A21"
TEXT = "#E6EAF2"
MUTED = "#9AA4B2"

ANALYTICS_DIR = Path("data/analytics")
PROCESSED_DIR = Path("data/processed")


@st.cache_data(show_spinner=False)
def load_data() -> dict[str, Any]:
    """Load analytics and processed datasets from local pipeline outputs."""
    data: dict[str, Any] = {
        "train_rankings": _load_json_list(ANALYTICS_DIR / "train_rankings.json"),
        "corridor_rankings": _load_json_list(ANALYTICS_DIR / "corridor_rankings.json"),
        "halt_efficiency": _load_json_list(ANALYTICS_DIR / "halt_efficiency.json"),
        "route_efficiency": _load_json_list(ANALYTICS_DIR / "route_efficiency.json"),
        "train_summaries": _load_json_list(PROCESSED_DIR / "train_summaries.json"),
        "route_segments": _load_json_list(PROCESSED_DIR / "route_segments.json"),
    }
    return data


def _load_json_list(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
    except (json.JSONDecodeError, OSError):
        return []
    return []


def _safe_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def compute_dashboard_metrics(data: dict[str, Any]) -> dict[str, Any]:
    """Compute executive KPIs and narrative primitives from loaded datasets."""
    train_rankings = data["train_rankings"]
    corridor_rankings = data["corridor_rankings"]
    halt_efficiency = data["halt_efficiency"]
    route_segments = data["route_segments"]

    top_train = train_rankings[0] if train_rankings else {}
    worst_corridor = corridor_rankings[-1] if corridor_rankings else {}

    speeds = [_safe_float(item.get("speedOnSectionKmph")) for item in corridor_rankings]
    speeds = [s for s in speeds if s is not None]
    avg_network_speed = round(sum(speeds) / len(speeds), 1) if speeds else None

    halt_vals = [_safe_float(item.get("haltDurationMinutes")) for item in halt_efficiency]
    halt_vals = [h for h in halt_vals if h is not None]
    avg_delay_proxy = round(sum(halt_vals) / len(halt_vals), 1) if halt_vals else None

    station_count: dict[str, int] = {}
    for item in halt_efficiency:
        station = str(item.get("stationCode") or "UNKNOWN")
        station_count[station] = station_count.get(station, 0) + 1
    worst_station = max(station_count, key=station_count.get) if station_count else "N/A"

    latest_ts = _latest_timestamp([
        ANALYTICS_DIR / "train_rankings.json",
        ANALYTICS_DIR / "corridor_rankings.json",
        PROCESSED_DIR / "route_segments.json",
    ])

    return {
        "active_trains": len(data["train_summaries"]),
        "snapshot_proxy": len(route_segments),
        "latest_ts": latest_ts,
        "top_train": top_train,
        "worst_corridor": worst_corridor,
        "avg_network_speed": avg_network_speed,
        "avg_delay_proxy": avg_delay_proxy,
        "worst_station": worst_station,
    }


def _latest_timestamp(paths: list[Path]) -> str:
    times = [p.stat().st_mtime for p in paths if p.exists()]
    if not times:
        return "N/A"
    return datetime.fromtimestamp(max(times)).strftime("%Y-%m-%d %H:%M")


def render_header(metrics: dict[str, Any]) -> None:
    st.markdown("""
    <div class='header-wrap'>
      <div>
        <div class='page-title'>Premium Railway Operational Intelligence</div>
        <div class='page-subtitle'>Reliability analytics for India's premium rail network</div>
      </div>
      <div class='chip-wrap'>
        <span class='chip'>Active Trains: {active}</span>
        <span class='chip'>Snapshots: {snapshots}</span>
        <span class='chip'>Latest Update: {latest}</span>
      </div>
    </div>
    """.format(
        active=metrics["active_trains"], snapshots=metrics["snapshot_proxy"], latest=metrics["latest_ts"]
    ), unsafe_allow_html=True)


def render_kpi_strip(metrics: dict[str, Any]) -> None:
    cols = st.columns(6)
    kpis = [
        ("Most Reliable Train", metrics["top_train"].get("trainName", "N/A"), True),
        ("Worst Performing Corridor", metrics["worst_corridor"].get("stationCode", "N/A"), False),
        ("Average Network Speed", f"{metrics['avg_network_speed']} km/h" if metrics["avg_network_speed"] else "N/A", False),
        ("Average Delay (Proxy)", f"{metrics['avg_delay_proxy']} min" if metrics["avg_delay_proxy"] else "N/A", False),
        ("Highest Congestion Junction", metrics["worst_station"], False),
        ("Operational Snapshots", str(metrics["snapshot_proxy"]), False),
    ]
    for idx, (label, value, accent) in enumerate(kpis):
        with cols[idx]:
            cls = "kpi-card accent" if accent else "kpi-card"
            st.markdown(f"<div class='{cls}'><div class='kpi-label'>{label}</div><div class='kpi-value'>{value}</div></div>", unsafe_allow_html=True)


def render_train_rankings(data: dict[str, Any]) -> None:
    st.subheader("Vande Bharat and Rajdhani segments separate clearly on efficiency-adjusted speed")
    rows = data["train_rankings"][:10]
    if not rows:
        st.info("Train ranking data not available.")
        return
    chart_data = []
    for idx, item in enumerate(rows):
        chart_data.append({
            "train": item.get("trainName") or item.get("trainNumber") or "Unknown",
            "score": _safe_float(item.get("avgSpeedKmph")) or 0.0,
            "color": ACCENT if idx == 0 else "#596273",
            "label": f"{_safe_float(item.get('avgSpeedKmph')) or 0:.1f}",
        })
    spec = {
        "mark": {"type": "bar", "cornerRadiusEnd": 3},
        "encoding": {
            "y": {"field": "train", "type": "ordinal", "sort": "-x", "axis": {"labelColor": TEXT}},
            "x": {"field": "score", "type": "quantitative", "axis": {"labelColor": TEXT, "gridColor": "#2A2F3A"}},
            "color": {"field": "color", "type": "nominal", "scale": None, "legend": None},
            "tooltip": [{"field": "train"}, {"field": "score"}],
        },
        "width": "container",
        "height": 340,
    }
    st.vega_lite_chart(chart_data, spec, use_container_width=True)


def render_corridor_analysis(data: dict[str, Any], top_n: int) -> None:
    st.subheader("Corridor bottlenecks concentrate around low-speed sections with repeated halt stress")
    rows = data["corridor_rankings"]
    if not rows:
        st.info("Corridor ranking data not available.")
        return
    ranked = sorted(rows, key=lambda r: (_safe_float(r.get("speedOnSectionKmph")) or 0.0))[:top_n]
    chart_data = [{
        "corridor": f"{r.get('trainNumber','?')} • {r.get('stationCode','?')}",
        "speed": _safe_float(r.get("speedOnSectionKmph")) or 0.0,
    } for r in ranked]
    spec = {
        "mark": {"type": "bar", "cornerRadiusEnd": 2, "color": "#6C7485"},
        "encoding": {
            "y": {"field": "corridor", "type": "ordinal", "sort": "x", "axis": {"labelColor": TEXT}},
            "x": {"field": "speed", "type": "quantitative", "axis": {"labelColor": TEXT, "gridColor": "#2A2F3A"}},
        },
        "height": 300,
    }
    st.vega_lite_chart(chart_data, spec, use_container_width=True)
    if ranked:
        st.caption(f"Delay spikes most where section speed falls to {chart_data[0]['speed']:.1f} km/h around {ranked[0].get('stationCode','N/A')}.")


def render_route_degradation(data: dict[str, Any], selected_train: str) -> None:
    st.subheader("Schedule adherence drops sharply after key junction clusters")
    segments = [r for r in data["route_segments"] if (r.get("trainNumber") or "") == selected_train]
    if not segments:
        st.info("Route segment data not available for selected train.")
        return
    segments = sorted(segments, key=lambda r: (int(r.get("day") or 0), int(r.get("sequence") or 0)))
    cumulative = 0.0
    points = []
    for seg in segments:
        halt = _safe_float(seg.get("haltDurationMinutes")) or 0.0
        cumulative += halt
        points.append({
            "x": f"D{seg.get('day','?')}-S{seg.get('sequence','?')}",
            "cum": round(cumulative, 2),
            "station": seg.get("stationCode") or "",
        })
    spec = {
        "mark": {"type": "line", "strokeWidth": 2, "color": ACCENT},
        "encoding": {
            "x": {"field": "x", "type": "ordinal", "axis": {"labels": False, "ticks": False, "title": "Route progression"}},
            "y": {"field": "cum", "type": "quantitative", "axis": {"labelColor": TEXT, "gridColor": "#2A2F3A", "title": "Cumulative halt minutes"}},
            "tooltip": [{"field": "station"}, {"field": "cum"}],
        },
        "height": 280,
    }
    st.vega_lite_chart(points, spec, use_container_width=True)


def render_halt_station_analysis(data: dict[str, Any]) -> None:
    st.subheader("Station-level halt inefficiency reveals recurring congestion hotspots")
    rows = data["halt_efficiency"]
    if not rows:
        st.info("Halt efficiency data not available.")
        return
    agg: dict[str, list[float]] = {}
    for row in rows:
        station = str(row.get("stationCode") or "UNKNOWN")
        halt = _safe_float(row.get("haltDurationMinutes"))
        if halt is None:
            continue
        agg.setdefault(station, []).append(halt)
    avg = [{"station": k, "avg_halt": round(sum(v) / len(v), 2)} for k, v in agg.items()]
    avg_sorted = sorted(avg, key=lambda x: x["avg_halt"], reverse=True)[:12]
    spec = {
        "mark": {"type": "bar", "color": "#697488"},
        "encoding": {
            "y": {"field": "station", "type": "ordinal", "sort": "-x", "axis": {"labelColor": TEXT}},
            "x": {"field": "avg_halt", "type": "quantitative", "axis": {"labelColor": TEXT, "gridColor": "#2A2F3A"}},
            "tooltip": [{"field": "station"}, {"field": "avg_halt"}],
        },
        "height": 320,
    }
    st.vega_lite_chart(avg_sorted, spec, use_container_width=True)


def render_insight_panel(data: dict[str, Any], metrics: dict[str, Any]) -> None:
    insights = []
    top = metrics["top_train"]
    if top:
        insights.append(f"Top reliability leader is {top.get('trainName','N/A')} at {top.get('avgSpeedKmph','N/A')} km/h average corridor speed proxy.")
    if metrics["worst_station"] != "N/A":
        insights.append(f"{metrics['worst_station']} appears most frequently in inefficient halt clusters, indicating repeat congestion exposure.")
    if metrics["avg_network_speed"] is not None:
        insights.append(f"Network-wide section speed averages {metrics['avg_network_speed']} km/h, providing a baseline for premium service benchmarking.")
    if metrics["avg_delay_proxy"] is not None:
        insights.append(f"Average halt delay proxy is {metrics['avg_delay_proxy']} minutes, signaling where timetable slack may be consumed.")

    st.subheader("Operational Intelligence Narrative")
    st.markdown("<div class='insight-box'>" + "<br/>".join([f"- {x}" for x in insights[:6]]) + "</div>", unsafe_allow_html=True)


def render_empty_state() -> None:
    st.warning("No processed analytics datasets were found. Run processors and KPI generation to populate `data/analytics` and `data/processed`.")


def apply_theme() -> None:
    st.set_page_config(page_title="Premium Railway Operational Intelligence", layout="wide")
    st.markdown(
        f"""
        <style>
        .stApp {{ background: {BG}; color: {TEXT}; }}
        .header-wrap {{ display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1rem; }}
        .page-title {{ font-size:2.0rem; font-weight:800; color:{TEXT}; letter-spacing:0.3px; }}
        .page-subtitle {{ color:{MUTED}; margin-top:0.2rem; }}
        .chip-wrap {{ display:flex; gap:0.5rem; flex-wrap:wrap; justify-content:flex-end; }}
        .chip {{ background:{CARD}; color:{MUTED}; padding:0.45rem 0.65rem; border-radius:999px; border:1px solid #232833; font-size:0.78rem; }}
        .kpi-card {{ background:{CARD}; border:1px solid #232833; border-radius:12px; padding:0.75rem; min-height:115px; box-shadow:0 3px 10px rgba(0,0,0,0.18); }}
        .kpi-card.accent {{ border-color:{ACCENT}; box-shadow:0 0 0 1px rgba(79,179,200,0.25); }}
        .kpi-label {{ color:{MUTED}; font-size:0.74rem; text-transform:uppercase; letter-spacing:0.6px; }}
        .kpi-value {{ color:{TEXT}; margin-top:0.4rem; font-size:1.2rem; font-weight:700; line-height:1.2; }}
        .insight-box {{ background:{CARD}; border:1px solid #232833; border-radius:12px; padding:1rem; color:{TEXT}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    apply_theme()
    data = load_data()
    if not (data["train_rankings"] or data["corridor_rankings"] or data["route_segments"]):
        render_empty_state()
        return

    metrics = compute_dashboard_metrics(data)
    render_header(metrics)
    render_kpi_strip(metrics)

    st.markdown("###")
    col1, col2 = st.columns([2, 1])
    with col1:
        render_train_rankings(data)
    with col2:
        top_n = st.slider("Bottleneck corridors (Top N)", min_value=5, max_value=25, value=10)
        render_corridor_analysis(data, top_n)

    st.markdown("###")
    trains = sorted({str(r.get("trainNumber")) for r in data["route_segments"] if r.get("trainNumber")})
    selected_train = st.selectbox("Route degradation train focus", trains, index=0 if trains else None)
    if selected_train:
        render_route_degradation(data, selected_train)

    st.markdown("###")
    render_halt_station_analysis(data)
    st.markdown("###")
    render_insight_panel(data, metrics)


if __name__ == "__main__":
    main()
