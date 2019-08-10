#!/usr/bin/python

from socket import *
from hashlib import sha1
import hmac

BUFFER_SIZE = 1024

s = socket(AF_INET, SOCK_STREAM)
s.connect(("172.16.190.128", 20003))

token = s.recv(BUFFER_SIZE)
token = token[1:(len(token)-2)] # remove "" from received token
print 'Token - ' + token

hash_ok = False
i = 0
while not hash_ok:
    json_template = '{"tags":["a", "b", "c"], "title": "Hello", "contents": "World", "serverip": "127.0.0.1", "count":' + str(i) + '}'
    request = token + json_template
    hmac_object = hmac.new(token, request, sha1)
    hmac_digest = hmac_object.hexdigest()
    # print hmac_digest
    i += 1
    first_two_bytes = hmac_digest[0:4]
    if first_two_bytes == "0000":
        hash_ok = True

print("valid hmac - " + hmac_digest)
print("send valid request (token + json_template) -\n" + request)
s.send(request)
s.close()
