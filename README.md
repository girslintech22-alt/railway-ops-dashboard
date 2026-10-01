# 🚆 Railway Operations Intelligence Dashboard

> **A data-driven railway operations analytics platform for monitoring train performance, identifying corridor bottlenecks, analyzing station-level congestion, and generating operational insights from train movement data.**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit\&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas\&logoColor=white)](https://pandas.pydata.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite\&logoColor=white)](https://www.sqlite.org/)
[![Vite](https://img.shields.io/badge/Vite-Frontend-646CFF?logo=vite\&logoColor=white)](https://vitejs.dev/)

---

## 📌 Overview

**Railway Operations Intelligence Dashboard** is an analytics platform designed to transform raw railway movement data into actionable operational insights.

The system collects train data through the **RailRadar API**, stores raw snapshots, processes train and route-level information, generates operational KPIs, and presents the resulting insights through an interactive dashboard.

Instead of simply displaying train locations, the project focuses on the **operational questions behind railway performance**:

* Which trains are performing consistently?
* Which corridors contain potential bottlenecks?
* Which stations experience repeated halt inefficiency?
* Where does cumulative schedule degradation occur along a route?
* What operational patterns can be extracted from historical train snapshots?

The application follows an end-to-end **data engineering → analytics → visualization** workflow.

---

## 🎯 Key Objectives

The project was built around four major objectives:

1. **Collect** structured railway movement data from an external API.
2. **Normalize and process** raw train and route snapshots into analytical datasets.
3. **Generate operational KPIs** for train, corridor, and station performance.
4. **Visualize insights** through an operations-focused dashboard.

---

## ✨ Features

### 🚆 Train Performance Analysis

Analyze train-level performance using metrics such as:

* Average speed
* Distance travelled
* Total halts
* Travel time
* Running days
* Source and destination stations
* Train type

Train-level rankings help identify consistently efficient services.

---

### 🛤️ Corridor Bottleneck Analysis

The dashboard identifies low-speed sections across train corridors.

It can highlight:

* Low-speed sections
* Potential bottleneck locations
* Repeated operational stress
* Train/station combinations requiring further investigation

Users can control the number of bottleneck corridors displayed using an interactive **Top-N selector**.

---

### 🚉 Station Halt Efficiency

Station-level analysis aggregates halt durations to identify locations where trains repeatedly spend more time than expected.

This helps surface:

* Congestion hotspots
* Repeated halt inefficiency
* Junction-level operational pressure

---

### 📉 Route Degradation Analysis

For a selected train, the dashboard tracks cumulative halt duration as the train progresses through its route.

This provides a visual representation of how operational delay proxies accumulate throughout a journey.

The analysis can help answer:

> **Where does operational degradation begin to accumulate along a train's route?**

---

### 📊 Operational KPI Dashboard

The dashboard provides an executive-level view containing metrics such as:

* Most reliable train
* Worst-performing corridor
* Average network speed
* Average halt-delay proxy
* Highest congestion junction
* Number of operational snapshots

The dashboard also generates a narrative insight section summarizing important patterns found in the processed data.

---

## 🏗️ System Architecture

```text
                  ┌─────────────────────┐
                  │     RailRadar API   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Data Ingestion    │
                  │  API Polling Layer  │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    Raw Snapshots    │
                  │      JSON Data      │
                  └──────────┬──────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │       Processing Layer       │
              │                              │
              │  • Train Processing          │
              │  • Route Processing           │
              │  • Data Validation            │
              └──────────────┬───────────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Analytics / KPI     │
                  │      Engine         │
                  └──────────┬──────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │    Processed Analytics       │
              │                              │
              │ • Train Rankings             │
              │ • Corridor Rankings          │
              │ • Route Efficiency            │
              │ • Halt Efficiency             │
              └──────────────┬───────────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Streamlit Dashboard │
                  └─────────────────────┘
```

---

## 🔄 Data Pipeline

The project uses a staged pipeline:

### 1. Ingestion

The ingestion layer requests train information from the RailRadar API.

API requests use:

* API-key authentication
* 12-second request timeout
* Up to 3 retry attempts
* Exponential backoff
* Structured logging

Raw responses are stored locally as timestamped JSON snapshots.

```text
RailRadar API
     ↓
API Poller
     ↓
Validation
     ↓
data/raw/*.json
```

---

### 2. Processing

Raw snapshots are transformed into normalized analytical datasets.

The processing layer extracts information such as:

```text
Train Number
Train Name
Train Type
Source Station
Destination Station
Total Halts
Distance
Average Speed
Travel Time
Running Days
```

Route-level processing additionally creates segment-level information for downstream corridor and halt analysis.

---

### 3. Analytics

The KPI engine converts processed data into analytical outputs including:

```text
train_rankings.json
corridor_rankings.json
route_efficiency.json
halt_efficiency.json
```

These datasets are consumed by the dashboard.

---

### 4. Visualization

The Streamlit application loads the processed datasets and renders:

* KPI cards
* Train rankings
* Corridor bottleneck charts
* Route degradation curves
* Station halt analysis
* Operational insight narratives

The dashboard also includes caching for efficient repeated data access.

---

## 📁 Project Structure

```text
railway-ops-dashboard/
│
├── analytics/
│   └── kpi_engine.py
│
├── config/
│   └── trains.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── analytics/
│
├── database/
│
├── docs/
│
├── ingestion/
│   └── poller.py
│
├── processing/
│   ├── route_processor.py
│   └── train_processor.py
│
├── src/
│
├── storage/
│
├── tests/
│
├── main.py
├── run_pipeline.py
├── test_railradar.py
│
├── requirements.txt
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── README.md
```

The repository separates **ingestion, processing, analytics, storage, testing, and presentation**, making the pipeline easier to extend and debug.

---

## 🛠️ Tech Stack

### Backend / Data

* **Python**
* **Requests** — API communication
* **python-dotenv** — environment variable management
* **Pandas** — data processing
* **SQLite** — local analytical storage

### Analytics

* KPI generation
* Train-level ranking
* Corridor analysis
* Halt-efficiency analysis
* Route-level degradation analysis

### Visualization

* **Streamlit**
* **Vega-Lite**
* Interactive controls and charts

### Frontend

The repository also contains a Vite-based frontend setup using:

* React
* Vite
* Tailwind CSS
* Recharts
* Framer Motion

The current Python dashboard is implemented through Streamlit, while the frontend dependencies provide a separate web UI foundation.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/girslintech22-alt/railway-ops-dashboard.git

cd railway-ops-dashboard
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

The current dependency file includes Requests, python-dotenv, Pytest, Streamlit, Pandas, and Plotly.

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
RAILRADAR_API_KEY=your_api_key_here
```

The ingestion layer reads the API key from `RAILRADAR_API_KEY` and sends it through the `X-API-Key` request header.

> **Never commit your API key or `.env` file to GitHub.**

---

## ▶️ Running the Pipeline

Run the complete ingestion → processing → analytics pipeline:

```bash
python run_pipeline.py
```

The pipeline performs:

```text
1. Train data ingestion
        ↓
2. Raw snapshot storage
        ↓
3. Train processing
        ↓
4. Route processing
        ↓
5. KPI generation
        ↓
6. Analytics dataset validation
```

The pipeline reports successful and failed API polls, generated snapshots, analytics file counts, and dataset validation results.

---

## 📊 Running the Dashboard

After the pipeline has generated the required datasets:

```bash
streamlit run main.py
```

Then open the local Streamlit URL shown in your terminal.

The dashboard expects processed analytics files under:

```text
data/analytics/
data/processed/
```

If those datasets are unavailable, the application displays an empty-state message instructing the user to run the processing and KPI generation pipeline.

---

## 🧪 Testing

Run the available tests using:

```bash
pytest
```

The repository includes a dedicated RailRadar test module:

```text
test_railradar.py
```

---

## 📈 Dashboard Sections

### 1. Executive KPI Strip

Provides a quick operational snapshot:

| KPI                         | Description                                                    |
| --------------------------- | -------------------------------------------------------------- |
| Most Reliable Train         | Highest-ranked train based on processed performance metrics    |
| Worst Performing Corridor   | Lowest-ranked corridor section                                 |
| Average Network Speed       | Average speed across analyzed sections                         |
| Average Delay Proxy         | Average halt-duration proxy                                    |
| Highest Congestion Junction | Station appearing most frequently in inefficient halt clusters |
| Operational Snapshots       | Number of processed route observations                         |

---

### 2. Train Rankings

Ranks the top train services using average corridor speed and related performance data.

---

### 3. Corridor Bottlenecks

Highlights the lowest-speed corridor sections.

The dashboard allows users to adjust the number of bottlenecks displayed.

---

### 4. Route Degradation

Users can select an individual train and inspect cumulative halt duration across its route.

---

### 5. Station Analysis

Aggregates halt duration by station to identify recurring congestion hotspots.

---

### 6. Operational Intelligence

Automatically generates concise observations from the analytical datasets, allowing users to move from **charts → patterns → operational interpretation**.

---

## 🔍 Example Analytical Questions

The platform is designed to answer questions such as:

### Train Performance

> Which train services demonstrate consistently higher average operating speed?

### Corridor Performance

> Which route sections repeatedly exhibit lower operating speeds?

### Station Congestion

> Which stations have the highest average halt duration?

### Route Degradation

> At what point during a train's journey does cumulative operational delay begin to increase significantly?

### Network Monitoring

> What are the current high-level indicators of network performance?

---

## 🧠 Engineering Approach

A key design principle of the project is separating **data collection from analytics and presentation**.

Instead of coupling the dashboard directly to an external API:

```text
API → Dashboard
```

the project follows:

```text
API
 ↓
Raw Data
 ↓
Processing
 ↓
Analytics
 ↓
Dashboard
```

This provides several advantages:

* Reproducible analysis
* Easier debugging
* Separation of concerns
* Ability to reprocess historical snapshots
* Reduced dependency on live API availability
* Easier testing of individual pipeline stages
* Cleaner dashboard logic

---

## ⚡ Reliability Considerations

The ingestion layer includes defensive API handling:

```text
Request
  ↓
12-second timeout
  ↓
Retry
  ↓
Exponential backoff
  ↓
Retry limit
  ↓
Persist successful response
```

This reduces the impact of temporary API failures and prevents a single failed train request from terminating the entire pipeline.

---

## 🚀 Future Improvements

Potential extensions include:

* Real-time train monitoring
* Historical delay trend analysis
* Delay prediction models
* Train-level anomaly detection
* Route reliability scoring
* Station congestion forecasting
* Weather/event-based delay analysis
* Automated operational alerts
* ML-based bottleneck prediction
* PostgreSQL deployment for larger datasets
* Role-based operational dashboards
* Cloud deployment and scheduled data ingestion

---

## ⚠️ Data & Usage Disclaimer

This project is an **independent analytics and visualization project** built for educational, engineering, and portfolio purposes.

It should not be interpreted as an official Indian Railways operational system.

Data availability and accuracy depend on the upstream API and the snapshots collected during pipeline execution.

---

## 👨‍💻 Author

**Ashu Jha**

B.Tech — Electronics & Communication Engineering

Interested in:

* Data Analytics
* Machine Learning
* AI/GenAI
* Product Management
* Data-driven Product Thinking

---

## ⭐ Project Focus

```text
Data Engineering
        +
Analytics
        +
Operational Intelligence
        +
Interactive Visualization
```

**From raw train movement data to operational insights.**
