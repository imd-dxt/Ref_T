from django.shortcuts import render, redirect, get_object_or_404
from .forms import URLScanForm
from .models import ScanResult
from .scanner import ZAPScanner
import logging

# Set up logging
logger = logging.getLogger(__name__)

def scan_url(request):
    if request.method == 'POST':
        form = URLScanForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['target_url']
            logger.info(f"Starting scan for URL: {url}")
            scanner = ZAPScanner(api_key='n00v2v1bm6u23d7ic1v2armusr')
            
            
            results = list(scanner.scan_urls_concurrently([url]))
            for url, report in results:
                if report:
                    logger.info(f"Scan completed for URL: {url}")

                    
                    result = ScanResult(
                        url=url,
                        scan_date=report['scan_date'],
                        high_risk_count=report['risk_summary']['High'],
                        medium_risk_count=report['risk_summary']['Medium'],
                        low_risk_count=report['risk_summary']['Low'],
                        informational_risk_count=report['risk_summary']['Informational'],
                        total_alerts=report['total_alerts'],
                        report=report
                    )
                    result.save()
                    return redirect('scan-results', pk=result.pk)
                else:
                    logger.error(f"Failed to scan URL: {url}")
        else:
            logger.error(f"Form is not valid: {form.errors}")
    else:
        form = URLScanForm()

    return render(request, 'scanner_app/scan_form.html', {'form': form})

def scan_results(request, pk):
    result = get_object_or_404(ScanResult, pk=pk)
    return render(request, 'scanner_app/scan_results.html', {'result': result})