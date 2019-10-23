#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The Python implementation of GiGA Genie gRPC client"""
from __future__ import print_function
import grpc
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import os
import datetime
import hmac
import hashlib

# Config for GiGA Genie gRPC
CLIENT_ID = 'Y2xpZW50X2lkMTU3MDY3NTM2MDA0Ng=='
CLIENT_KEY = 'Y2xpZW50X2tleTE1NzA2NzUzNjAwNDY='
CLIENT_SECRET = 'Y2xpZW50X3NlY3JldDE1NzA2NzUzNjAwNDY='
HOST = 'connector.gigagenie.ai'
PORT = 4080

### COMMON : Client Credentials ###
def getMetadata():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    message = CLIENT_ID + ':' + timestamp

    #python 3.x
    #CLIENT_SECRET_BYTES = bytes(CLIENT_SECRET, 'utf-8')
    #message_bytes = bytes(message, 'utf-8')
    #signature = hmac.new(CLIENT_SECRET_BYTES, message_bytes, hashlib.sha256).hexdigest()

    #python 2.x
    CLIENT_SECRET_BYTES = bytes(CLIENT_SECRET).encode('utf-8')
    message_bytes = bytes(message).encode('utf-8')
    signature = hmac.new(CLIENT_SECRET, message, hashlib.sha256).hexdigest()

    metadata = [('x-auth-clientkey', CLIENT_KEY),
                ('x-auth-timestamp', timestamp),
                ('x-auth-signature', signature)]
    return metadata

def credentials(context, callback):
    callback(getMetadata(), None)

def getCredentials():
    with open('ca-bundle.pem', 'rb') as f:
        trusted_certs = f.read()

    sslCred = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    authCred = grpc.metadata_call_credentials(credentials)
    return grpc.composite_channel_credentials(sslCred, authCred)
### END OF COMMON ###

# TTS : getText2VoiceURL
def getText2VoiceUrl(text):
    channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), getCredentials())
    stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)

    message = gigagenieRPC_pb2.reqText()
    message.text = text
    message.mode = 0
    message.lang = 0

    response = stub.getText2VoiceUrl(message)
    print ("resultCd: %d" % (response.resultCd))

    if response.resultCd == 200:
        print ("url: %s" % (response.url))

    else:
        print ("Fail: %d" % (response.resultCd))
        #return None
def main():
    getText2VoiceUrl("안녕하세요. 반갑습니다.")

if __name__ == '__main__':
    main()