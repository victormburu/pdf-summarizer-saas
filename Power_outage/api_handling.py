import requests
import json
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from pathlib import Path
from datetime import datetime, timedelta
from config import API_URL, API_HEADERS, API_PAYLOAD, CACHE_FILE, WATCH_AREAS

class OutageAPI:
    def __init__(self):
        """Initialize with configuration from config.py"""
        self.base_url = API_URL
        self.session = requests.Session()
        self.session.headers.update(API_HEADERS)
        self.default_payload = API_PAYLOAD
        self.cache_file = Path(CACHE_FILE)
        self.cache_file.parent.mkdir(exist_ok=True)
        self.last_success = None
        self.default_outages = self._create_default_outages()

    def _create_default_outages(self):
        """Create default outage data structure for watch areas without duplicates"""
        return {
            'data': [
                {
                    'area': area,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'reason': 'Status unknown - API unavailable',
                    'time': 'Check with provider',
                    'source': 'default'
                } for area in set(WATCH_AREAS)  # Use set to remove duplicates
            ],
            'timestamp': datetime.now().isoformat(),
            'source': 'default'
        }

    @retry(stop=stop_after_attempt(2),
          wait=wait_exponential(multiplier=1, min=2, max=5),
          reraise=True)
    def _try_fetch_outages(self):
        """Internal method to try fetching outages with timeout"""
        try:
            response = self.session.post(
                self.base_url,
                json=self.default_payload,
                timeout=(3, 7)  # Connect timeout 3s, read timeout 7s
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.warning(f"API request attempt failed: {str(e)}")
            raise

    def _get_fresh_outages(self):
        """Get fresh outages with success tracking"""
        try:
            data = self._try_fetch_outages()
            self.last_success = datetime.now()
            self._save_cache(data)
            return data
        except Exception as e:
            logging.error(f"Failed to get fresh outages: {str(e)}")
            raise

    def _save_cache(self, data):
        """Save data to cache file with validation"""
        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'data': data,
                'source': 'api'
            }
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
            logging.debug("Successfully saved cache")
        except Exception as e:
            logging.error(f"Failed to save cache: {str(e)}")

    def _load_cache(self):
        """Load and validate cached data"""
        try:
            if not self.cache_file.exists():
                logging.info("No cache file exists")
                return None

            with open(self.cache_file, 'r') as f:
                cache = json.load(f)

            # Validate cache structure
            if not isinstance(cache, dict):
                raise ValueError("Invalid cache format")
            if 'data' not in cache:
                raise ValueError("Missing data in cache")
            if 'timestamp' not in cache:
                raise ValueError("Missing timestamp in cache")

            # Check if cache is stale (>12 hours old)
            cache_time = datetime.fromisoformat(cache['timestamp'])
            if datetime.now() - cache_time > timedelta(hours=12):
                logging.warning("Cache is stale (older than 12 hours)")
                return None

            return cache['data']
        except json.JSONDecodeError:
            logging.error("Cache file corrupted - creating fresh cache")
            self._save_cache(self.default_outages)
            return None
        except Exception as e:
            logging.error(f"Cache load error: {str(e)}")
            return None

    def get_outages(self):
        """Main method to get outages with multiple fallback options"""
        # First try fresh data
        try:
            return self._get_fresh_outages()
        except Exception as fresh_error:
            logging.warning("Failed to get fresh data, trying cache...")
            
            # Try loading from cache
            cached = self._load_cache()
            if cached:
                logging.info("Using cached outage data")
                return cached
                
            logging.warning("No valid cached data available, using default data")
            return self.default_outages['data']