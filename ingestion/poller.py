import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

from config.trains import PREMIUM_TRAINS

BASE_URL = "https://api.railradar.org/api/v1/trains"
RAW_DIR = Path("data/raw")
TIMEOUT_SECONDS = 12
MAX_RETRIES = 3
BACKOFF_BASE_SECONDS = 2


def setup_logging() -> None:
    """Configure structured logging for poller runs."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s event=%(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )


def get_api_key() -> str:
    """Load and validate API key from environment."""
    load_dotenv()
    api_key = (os.getenv("RAILRADAR_API_KEY") or "").strip()
    if not api_key:
        raise ValueError("Missing RAILRADAR_API_KEY in .env")
    return api_key


def get_headers(api_key: str) -> Dict[str, str]:
    """Build request headers."""
    return {"X-API-Key": api_key}


def fetch_train_data(train_number: str, headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """Fetch train data with timeout and exponential backoff retry."""
    url = f"{BASE_URL}/{train_number}"
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=headers, timeout=TIMEOUT_SECONDS)
            if response.status_code == 200:
                return response.json()

            logging.warning(
                "api_non_200 train=%s attempt=%s status_code=%s",
                train_number,
                attempt,
                response.status_code,
            )
        except requests.Timeout:
            logging.warning("api_timeout train=%s attempt=%s", train_number, attempt)
        except requests.RequestException as exc:
            logging.warning("api_request_error train=%s attempt=%s error=%s", train_number, attempt, exc)
        except ValueError as exc:
            logging.warning("api_invalid_json train=%s attempt=%s error=%s", train_number, attempt, exc)
            return None

        if attempt < MAX_RETRIES:
            sleep_seconds = BACKOFF_BASE_SECONDS ** (attempt - 1)
            time.sleep(sleep_seconds)

    logging.error("api_failed_after_retries train=%s retries=%s", train_number, MAX_RETRIES)
    return None


def save_raw_response(train_number: str, payload: Dict[str, Any]) -> Path:
    """Persist raw API payload to disk."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = RAW_DIR / f"{train_number}_{timestamp}.json"
    with output_path.open("w", encoding="utf-8") as file_obj:
        json.dump(payload, file_obj, ensure_ascii=False, indent=2)
    return output_path


def poll_premium_trains() -> None:
    """Sequentially poll configured premium trains and store raw responses."""
    setup_logging()
    api_key = get_api_key()
    headers = get_headers(api_key)

    logging.info("poll_start train_count=%s", len(PREMIUM_TRAINS))
    for train in PREMIUM_TRAINS:
        train_number = str(train.get("train_no", "")).strip()
        if not train_number:
            logging.warning("skip_invalid_train_config train=%s", train)
            continue

        logging.info("poll_train_start train=%s", train_number)
        data = fetch_train_data(train_number, headers)
        if data is None:
            logging.error("poll_train_failed train=%s", train_number)
            continue

        output_path = save_raw_response(train_number, data)
        logging.info("poll_train_success train=%s file=%s", train_number, output_path)

    logging.info("poll_complete")


if __name__ == "__main__":
    poll_premium_trains()
