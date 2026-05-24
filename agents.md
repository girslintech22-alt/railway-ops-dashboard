# AGENTS.md

## Project Overview

This project is a Railway Reliability Analytics Platform focused on premium Indian trains:
- Rajdhani
- Duronto
- Vande Bharat

Goal:
Identify operational bottlenecks, delay patterns, and route reliability trends using sampled railway API data.

The system is optimized for a strict API limit of 1000 calls/month.

---

# Architecture

Pipeline:

API -> Raw JSON Storage -> Validation -> PostgreSQL -> Analytics -> Dashboard

Key principles:
1. Preserve raw API responses
2. Never discard source data
3. Minimize API usage
4. Prefer incremental updates
5. Handle API failures gracefully

---

# Tech Stack

Backend:
- Python
- Requests / AsyncIO
- PostgreSQL
- Pydantic

Analytics:
- Pandas
- NumPy

Visualization:
- Streamlit

Automation:
- GitHub Actions / Cron

---

# Coding Rules

## General
- Keep functions small and modular
- Avoid rewriting entire files
- Prefer patching only necessary sections
- Add docstrings for all public functions
- Use type hints everywhere

## API Usage
- Never make unnecessary API calls
- Use exponential backoff for retries
- Cache responses when possible

## Database
- Raw JSON must always be preserved
- Use JSONB for raw payload storage
- Add indexes only when necessary

## Analytics
- Prefer vectorized pandas operations
- Avoid nested loops on large datasets
- Keep transformations reproducible

## Dashboard
- Keep charts simple and fast
- Avoid loading full datasets in memory
- Use caching in Streamlit

---

# Expected Output Style

When generating code:
1. Explain reasoning briefly
2. Modify only relevant files
3. Avoid unnecessary abstractions
4. Include edge-case handling
5. Add logging where useful

---

# Important Business Context

Main analytical goals:
- Detect bottleneck stations
- Compare premium train punctuality
- Identify weekday reliability trends
- Build route reliability rankings

Important constraints:
- 1000 API calls/month
- Data may be incomplete
- APIs may fail intermittently