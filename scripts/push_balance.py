from db import Db
import base64
import hashlib
import requests
import time
import simplejson
#import our models
from payments.models import Balance

url = 'https://ekabet.com/api/v1/payments/balances/mpesa/'








def run():
	while True:
		balance = Balance.objects.get(pk=1)
		print(balance,"balance")
		utility_balance = balance.utility_balance
		working_balance = balance.working_balance
		payload = {
			'utility_balance':utility_balance,
			'working_balance':working_balance
		}

		print(payload,"PAYLOAD")

		# try:
		r = requests.post(url,json=payload)
		print(r.json())

		# except:
		# 	pass


	time.sleep(2)


#runs
run()
