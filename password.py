import base64
Timestamp='20180615121533'
BusinessShortCode='642086'
PASS_KEY='d433b8be80b9e35a722dbb1757d77623ee2448de4bb5fdd36878327d51ff81ac'
string=(BusinessShortCode+PASS_KEY+Timestamp).encode('utf-8')
encoded=base64.b64encode(string)
print(encoded)