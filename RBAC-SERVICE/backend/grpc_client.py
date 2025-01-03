import grpc
import scan_pb2
import scan_pb2_grpc

def scan_url(url):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = scan_pb2_grpc.ScanServiceStub(channel)
        response = stub.ScanUrl(scan_pb2.ScanRequest(url=url))
        return response.status, response.report