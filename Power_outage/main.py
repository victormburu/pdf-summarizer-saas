import logging
from datetime import datetime
from api_handling import OutageAPI
from config import WATCH_AREAS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('outage_monitor.log'),
        logging.StreamHandler()
    ]
)

def find_relevant_outages(outage_data, watch_areas):
    """Filter outages with case-insensitive matching and deduplication"""
    relevant = []
    seen_outages = set()  # Track seen outages to avoid duplicates
    
    if not outage_data or not isinstance(outage_data, list):
        logging.error("Invalid outage data format")
        return relevant
        
    for outage in outage_data:
        try:
            area = str(outage.get('area', '')).strip().lower()
            outage_date = outage.get('date', 'Unknown date')
            outage_time = outage.get('time', 'Unknown time')
            reason = outage.get('reason', 'Unknown reason')
            source = outage.get('source', 'api')
            
            # Create unique identifier for deduplication
            outage_id = f"{area}-{outage_date}-{outage_time}"
            
            if (outage_id not in seen_outages and 
                any(watch_area.lower() in area for watch_area in watch_areas)):
                
                seen_outages.add(outage_id)
                relevant.append({
                    'area': outage.get('area'),
                    'date': outage_date,
                    'time': outage_time,
                    'reason': reason,
                    'source': source
                })
        except Exception as e:
            logging.warning(f"Skipping invalid outage record: {str(e)}")
    return relevant

def main():
    logging.info("Starting outage monitor")
    
    try:
        api = OutageAPI()
        outages = api.get_outages()
        relevant = find_relevant_outages(outages, WATCH_AREAS)
        
        if relevant:
            # Count unique areas
            area_counts = {}
            for outage in relevant:
                area = outage['area']
                area_counts[area] = area_counts.get(area, 0) + 1
            
            logging.info(f"Found {len(relevant)} outage events across {len(area_counts)} areas:")
            
            for outage in relevant:
                status = (f"{outage['area']} - Date: {outage['date']} "
                         f"Time: {outage['time']} - Reason: {outage['reason']}")
                
                if outage.get('source') == 'default':
                    status += " (⚠️ DEFAULT DATA - API unavailable)"
                elif outage.get('source') == 'cache':
                    status += " (📦 CACHED DATA)"
                
                logging.info(f"• {status}")
            
            # Summary
            logging.info(f"Summary: {len(relevant)} outage events in {len(area_counts)} areas")
            
        else:
            logging.info("✅ No outages reported in monitored areas")
            
    except Exception as e:
        logging.critical(f"Monitor crashed: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()