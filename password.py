import base64
Timestamp='20190603121533'
BusinessShortCode='286630'
PASS_KEY='dbdcfbdb9a4ff9ad1ae49f2e9a3ccbca32fd83edfa923ba4d9923b1ef29051a0'
string=(BusinessShortCode+PASS_KEY+Timestamp).encode('utf-8')
encoded=base64.b64encode(string)
print(encoded)