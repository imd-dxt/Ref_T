import time
from zapv2 import ZAPv2
from datetime import datetime
import logging
import concurrent.futures

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ZAPScanner:
    def __init__(self, api_key, proxy_address='http://127.0.0.1:8080'):
        """Initialize ZAP scanner with API key and proxy address."""
        self.zap = ZAPv2(apikey=api_key, proxies={'http': proxy_address, 'https': proxy_address})
        self.scan_id = None

    def spider_url(self, target_url):
        """Spider the target URL before scanning."""
        try:
            logger.info(f"Starting spider for URL: {target_url}")
            spider_scan_id = self.zap.spider.scan(target_url)
            while True:
                status = self.zap.spider.status(spider_scan_id)
                if status == "100":
                    break
                time.sleep(2)
            logger.info(f"Spider completed for URL: {target_url}")
            return True
        except Exception as e:
            logger.error(f"Error during spidering: {str(e)}")
            return False

    def start_scan(self, target_url):
        """Start an active scan against the target URL."""
        if not self.spider_url(target_url):
            return False
        try:
            logger.info(f"Starting scan for URL: {target_url}")
            self.scan_id = self.zap.ascan.scan(target_url)
            return True
        except Exception as e:
            logger.error(f"Error starting scan: {str(e)}")
            return False

    def wait_for_scan_completion(self, check_interval=5):
        """Wait for the active scan to complete."""
        while True:
            status = self.get_scan_status()
            if status == "100":
                logger.info("Scan completed")
                return True
            time.sleep(check_interval)

    def get_scan_status(self):
        """Get the current status of the active scan."""
        if self.scan_id:
            return self.zap.ascan.status(self.scan_id)
        return None

    def generate_report(self):
        """Generate a detailed report of all findings."""
        alerts = self.zap.core.alerts()
        return {
            'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_alerts': len(alerts),
            'risk_summary': {
                'High': len([a for a in alerts if a['risk'] == 'High']),
                'Medium': len([a for a in alerts if a['risk'] == 'Medium']),
                'Low': len([a for a in alerts if a['risk'] == 'Low']),
                'Informational': len([a for a in alerts if a['risk'] == 'Informational'])
            },
            'alerts': alerts
        }

    def scan_urls_concurrently(self, urls):
        """Scan multiple URLs concurrently."""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.start_scan, url): url for url in urls}
            for future in concurrent.futures.as_completed(futures):
                url = futures[future]
                try:
                    future.result()
                    self.wait_for_scan_completion()
                    report = self.generate_report()
                    logger.info(f"Scan completed for URL: {url}")
                    yield url, report
                except Exception as e:
                    logger.error(f"Error scanning {url}: {str(e)}")
                    yield url, None