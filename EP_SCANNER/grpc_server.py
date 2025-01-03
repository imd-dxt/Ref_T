import os
import django
import grpc
from concurrent import futures
import logging
import scan_pb2
import scan_pb2_grpc

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EP_SCANNER.settings')
django.setup()

from scanner.views import VirusTotalScanner, ZAPScanner

class ScanService(scan_pb2_grpc.ScanServiceServicer):
    def ScanUrl(self, request, context):
        target_url = request.url
        # Perform the scan using existing logic
        vt_result = VirusTotalScanner.scan_url(target_url)
        zap_scanner = ZAPScanner(api_key='n00v2v1bm6u23d7ic1v2armusr')
        zap_scanner.start_scan(target_url)
        zap_scanner.wait_for_scan_completion()
        report = zap_scanner.generate_report(target_url)
        return scan_pb2.ScanResponse(status="Completed", report=str(report))

def serve():
    logging.basicConfig(level=logging.INFO)
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        scan_pb2_grpc.add_ScanServiceServicer_to_server(ScanService(), server)
        server.add_insecure_port('[::]:50051')
        logging.info("Starting gRPC server on port 50051...")
        server.start()
        logging.info("gRPC server is running.")
        server.wait_for_termination()
    except Exception as e:
        logging.error(f"Failed to start gRPC server: {e}")

if __name__ == '__main__':
    serve()