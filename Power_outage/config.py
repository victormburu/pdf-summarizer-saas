from pathlib import Path
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('outage_monitor.log'),
        logging.StreamHandler()
    ]
)

today = datetime.today()
thirty_days_ago = today - timedelta(days=30)

# API Configuration
API_URL = "https://api.nijulishe.co.ke/v1/rora/searchOutages"
API_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Origin": "https://nijulishe.co.ke",
    "Referer": "https://nijulishe.co.ke/"
}
API_PAYLOAD = {
    "searchTerm": "Nairobi",
    "startDate": thirty_days_ago.strftime("%Y-%m-%d"),
    "endDate": today.strftime("%Y-%m-%d")
}
# File Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
WATCH_AREAS_FILE = DATA_DIR / "watch_areas.txt"
CACHE_FILE = DATA_DIR / "outage_cache.json"
LOG_FILE = BASE_DIR / "logs/outage_monitor.log"
LOG_FILE.parent.mkdir(exist_ok=True)

# Load Watch Areas
try:
    with open(WATCH_AREAS_FILE, 'r', encoding='utf-8') as f:
        WATCH_AREAS = [line.strip() for line in f if line.strip()]
    if not WATCH_AREAS:
        raise ValueError("Watch areas file is empty")
    logging.info(f"Loaded {len(WATCH_AREAS)} watch areas")
except Exception as e:
    logging.critical(f"Failed to load watch areas: {e}")
    # Fallback to hardcoded list
    WATCH_AREAS = [
        "Roysambu", "Zimmerman", "Githurai 44", "Maziwa", "Kahawa West",
        "Kahawa Wendani", "Githurai 45", "Kasarani", "Seasons", "Hunters",
        "Sunton", "Mwiki", "Saika", "Kayole", "Umoja 2", "Umoja 3",
        "Umoja Innercore", "Kariobangi South", "Mathare North", "Huruma",
        "Imara Daima estate", "Dandora", "Lucky Summer", "Baba Dogo",
        "Nyayo estate", "Kwa Njenga", "Embakasi Pipeline estate",
        "Hazina estate", "Makongeni", "Kibera"
    ]