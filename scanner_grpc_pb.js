// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('@grpc/grpc-js');
var scanner_pb = require('./scanner_pb.js');

function serialize_scanner_ScanRequest(arg) {
  if (!(arg instanceof scanner_pb.ScanRequest)) {
    throw new Error('Expected argument of type scanner.ScanRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_scanner_ScanRequest(buffer_arg) {
  return scanner_pb.ScanRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_scanner_ScanResponse(arg) {
  if (!(arg instanceof scanner_pb.ScanResponse)) {
    throw new Error('Expected argument of type scanner.ScanResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_scanner_ScanResponse(buffer_arg) {
  return scanner_pb.ScanResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


var ScannerServiceService = exports.ScannerServiceService = {
  scanUrl: {
    path: '/scanner.ScannerService/ScanUrl',
    requestStream: false,
    responseStream: false,
    requestType: scanner_pb.ScanRequest,
    responseType: scanner_pb.ScanResponse,
    requestSerialize: serialize_scanner_ScanRequest,
    requestDeserialize: deserialize_scanner_ScanRequest,
    responseSerialize: serialize_scanner_ScanResponse,
    responseDeserialize: deserialize_scanner_ScanResponse,
  },
};

exports.ScannerServiceClient = grpc.makeGenericClientConstructor(ScannerServiceService);
