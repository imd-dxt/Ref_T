import time
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Scan, Alert
from zapv2 import ZAPv2
from datetime import datetime
import json
import logging
import requests
from bs4 import BeautifulSoup
from django.db.models import Case, When, Value, IntegerField

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# VirusTotal configuration
VIRUSTOTAL_API_KEY = "065820c901093f7d3117fa84549c5225d7e1e5f1739bc5bc19f5175899ff9bf1"
VIRUSTOTAL_URL = "https://www.virustotal.com/api/v3/urls"

# BuiltWith API configuration
BUILTWITH_API_KEY = "79774999-b28e-437b-8350-43b4697c9aed"  # Replace with your BuiltWith API key
BUILTWITH_API_URL = "https://api.builtwith.com/v20/api.json"

class VirusTotalScanner:
    @staticmethod
    def scan_url(target_url):
        headers = {
            "x-apikey": VIRUSTOTAL_API_KEY
        }
        try:
            response = requests.post(VIRUSTOTAL_URL, headers=headers, data={"url": target_url})
            if response.status_code == 200:
                logger.info("URL submitted to VirusTotal for scanning.")
                return response.json()
            else:
                logger.error(f"Error submitting URL to VirusTotal: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error during VirusTotal URL submission: {e}")
            return None

    @staticmethod
    def get_scan_results(analysis_id):
        headers = {
            "x-apikey": VIRUSTOTAL_API_KEY
        }
        try:
            result_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
            response = requests.get(result_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error retrieving VirusTotal scan results: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error retrieving VirusTotal scan results: {e}")
            return None

    @staticmethod
    def scan_domain(domain):
        headers = {
            "x-apikey": VIRUSTOTAL_API_KEY
        }
        try:
            url = f"https://www.virustotal.com/api/v3/domains/{domain}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return {
                    "detected_urls": len(data.get("data", {}).get("attributes", {}).get("last_analysis_results", {})),
                    "detected_communicating_samples": len(data.get("data", {}).get("attributes", {}).get("communicating_files", [])),
                    "categories": data.get("data", {}).get("attributes", {}).get("categories", {}),
                    "whois": data.get("data", {}).get("attributes", {}).get("whois", "Not available"),
                    "reputation": data.get("data", {}).get("attributes", {}).get("reputation", "Not available"),
                    "last_analysis_stats": data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}),
                    "subdomains": data.get("data", {}).get("attributes", {}).get("subdomains", []),
                    "resolutions": data.get("data", {}).get("attributes", {}).get("resolutions", [])
                }
            else:
                logger.error(f"Error retrieving VirusTotal domain report: {response.text}")
                return {"error": f"VT API error: {response.status_code}"}
        except Exception as e:
            logger.error(f"Error during VirusTotal domain scan: {e}")
            return {"error": f"VT scan failed: {str(e)}"}

class BuiltWithScanner:
    @staticmethod
    def get_technologies(target_url):
        params = {
            "KEY": BUILTWITH_API_KEY,
            "LOOKUP": target_url
        }
        try:
            response = requests.get(BUILTWITH_API_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                technologies = []
                if "Results" in data:
                    for result in data["Results"]:
                        for tech in result.get("Technologies", []):
                            technologies.append({
                                "name": tech.get("Name", "N/A"),
                                "description": tech.get("Description", "N/A"),
                                "category": tech.get("Categories", ["N/A"])[0]
                            })
                return technologies
            else:
                logger.error(f"Error retrieving BuiltWith data: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error during BuiltWith API request: {e}")
            return None

class ZAPScanner:
    def __init__(self, api_key, proxy_address='http://127.0.0.1:8080'):
        self.zap = ZAPv2(apikey=api_key, proxies={'http': proxy_address, 'https': proxy_address})
        self.scan_id = None

    def spider_url(self, target_url):
        try:
            logger.info(f"Starting spider for {target_url}")
            spider_scan_id = self.zap.spider.scan(target_url)
            while True:
                status = self.zap.spider.status(spider_scan_id)
                logger.info(f"Spider progress: {status}%")
                if status == "100":
                    logger.info("Spider completed successfully.")
                    break
                time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"Error during spider: {e}")
            return False

    def start_scan(self, target_url):
        try:
            if not self.spider_url(target_url):
                return False
            logger.info(f"Starting active scan for {target_url}")
            self.scan_id = self.zap.ascan.scan(target_url)
            return True
        except Exception as e:
            logger.error(f"Error starting active scan: {e}")
            return False

    def wait_for_scan_completion(self, check_interval=5):
        if not self.scan_id:
            logger.error("No active scan ID found.")
            return False
        while True:
            status = self.zap.ascan.status(self.scan_id)
            if status == "100":
                logger.info("Scan completed successfully.")
                return True
            logger.info(f"Scan progress: {status}%")
            time.sleep(check_interval)

    def get_alerts(self, risk_level=None):
        try:
            alerts = self.zap.core.alerts()
            if risk_level:
                alerts = [alert for alert in alerts if alert['risk'] == risk_level]
            return alerts
        except Exception as e:
            logger.error(f"Error retrieving alerts: {e}")
            return []

    def format_alert(self, alert):
        return {
            'risk_level': alert['risk'],
            'confidence': alert['confidence'],
            'name': alert['name'],
            'description': alert['description'],
            'url': alert['url'],
            'param': alert['param'],
            'evidence': alert.get('evidence', 'N/A'),
            'solution': alert.get('solution', 'N/A'),
            'reference': alert.get('reference', 'N/A'),
            'cwe_id': alert.get('cweid', 'N/A'),
            'wasc_id': alert.get('wascid', 'N/A')
        }

    
    def extract_technologies_from_evidence(self, evidence):
        """
        Extract server names, programming languages, and other details from evidence.
        Returns a set of unique technologies.
        """
        technologies = set()

        # Common server names
        servers = ["Apache", "nginx", "IIS", "Tomcat", "Node.js", "Express", "LiteSpeed", "Ubuntu", "Debian", "CentOS"]
        for server in servers:
            if server.lower() in evidence.lower():
                technologies.add((server, "Web Server"))

        # Programming languages
        languages = ["PHP", "Python", "Ruby", "Java", "JavaScript", "C#", "Go", "Swift", "Kotlin", "Perl", "Rust"]
        for lang in languages:
            if lang.lower() in evidence.lower():
                technologies.add((lang, "Programming Language"))

        return technologies

    def generate_report(self, target_url, risk_level=None):
        alerts = self.get_alerts(risk_level=risk_level)
        technologies = set()

        builtwith_tech = BuiltWithScanner.get_technologies(target_url)
        if builtwith_tech:
            for tech in builtwith_tech:
                technologies.add((tech["name"], tech["category"]))

        # Add technologies from evidence in alerts
        for alert in alerts:
            evidence = alert.get("evidence", "")
            if evidence:
                technologies.update(self.extract_technologies_from_evidence(evidence))

        # Convert set to list of dictionaries for JSON serialization
        technologies_list = [{"name": name, "category": category} for name, category in technologies]

        report = {
            'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_alerts': len(alerts),
            'risk_summary': {
                'High': len([a for a in alerts if a['risk'] == 'High']),
                'Medium': len([a for a in alerts if a['risk'] == 'Medium']),
                'Low': len([a for a in alerts if a['risk'] == 'Low']),
                'Informational': len([a for a in alerts if a['risk'] == 'Informational'])
            },
            'alerts': [self.format_alert(alert) for alert in alerts],
            'technologies': technologies_list
        }
        return report
def scan_view(request):
    if request.method == 'POST':
        target_url = request.POST.get('target_url')
        if target_url:
            # VirusTotal scan
            vt_result = VirusTotalScanner.scan_url(target_url)
            if vt_result and 'data' in vt_result:
                analysis_id = vt_result['data']['id']
                vt_scan_results = VirusTotalScanner.get_scan_results(analysis_id)
                logger.info(f"VirusTotal scan results: {vt_scan_results}")

            # Domain scan
            domain = target_url.split('//')[-1].split('/')[0]  # Extract domain from URL
            vt_domain_results = VirusTotalScanner.scan_domain(domain)
            logger.info(f"VirusTotal domain scan results: {vt_domain_results}")

            # ZAP scan
            scanner = ZAPScanner(api_key='sjr7fi42ofcab237q0h1rj49g2')
            if scanner.start_scan(target_url):
                scanner.wait_for_scan_completion()
                report = scanner.generate_report(target_url)
                report['vt_domain_results'] = vt_domain_results

                # Save scan and alerts
                scan = Scan.objects.create(target_url=target_url, status='Completed', report=report)
                for alert in report['alerts']:
                    Alert.objects.create(scan=scan, **alert)

                return redirect('scan_results', scan_id=scan.id)
    return render(request, 'scannerr/scan_form.html')
def scan_results_view(request, scan_id):
    scan = Scan.objects.get(id=scan_id)
    
    # Define the order of risk levels
    risk_order = Case(
        When(risk_level='High', then=Value(0)),
        When(risk_level='Medium', then=Value(1)),
        When(risk_level='Low', then=Value(2)),
        When(risk_level='Informational', then=Value(3)),
        default=Value(4),
        output_field=IntegerField(),
    )
    
    # Sort alerts by risk level
    alerts = scan.alerts.annotate(risk_order=risk_order).order_by('risk_order')
     # Process WHOIS data to remove duplicates
    if 'vt_domain_results' in scan.report and 'whois' in scan.report['vt_domain_results']:
        whois_data = scan.report['vt_domain_results']['whois']
        # Split WHOIS data into lines and filter duplicates
        whois_lines = whois_data.split('\n')
        unique_whois = {}
        for line in whois_lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if key not in unique_whois:
                    unique_whois[key] = value
        scan.report['vt_domain_results']['whois'] = unique_whois
    else:
        scan.report['vt_domain_results']['whois'] = {}
    context = {
        'scan': scan,
        'alerts': alerts,
        'vt_domain_results': scan.report.get('vt_domain_results', {})  # Ensure this key exists in the report
    }
    
    return render(request, 'scannerr/scan_results.html', context)