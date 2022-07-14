from db import Db
import base64
import hashlib
import requests
from requests.auth import HTTPBasicAuth
import time
import simplejson
#import our models
from payments.models import RawCheckout


CallBackURL = 'https://104.248.35.188:2020/ipn/checkout-response/'
PASSWORD = 'Mjk5NTMzNTNiNTNmZGNiMjE1MjZkYTQ1ODdjZjFmNjg1OTRmOGMxZmRlMWU3YmIzNzVhMGY0MzM3ZmRlMDdmODFjM2I5ZjIwMTgxMTI4MTMyODQ3'

CONSUMER_KEY = 'gvoZQPP6RADYnQ1Z1HK1WRkTLcVXckaK'
CONSUMER_SECRET = 'iTvEapPSfjpdpPf9'
TOKEN_URL = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


def generate_token():

	consumer_key = CONSUMER_KEY
	consumer_secret = CONSUMER_SECRET

	r = requests.get(TOKEN_URL,auth=HTTPBasicAuth(consumer_key, consumer_secret))
	token = r.json()

	return token.get('access_token')



def run():
    ROWS_SELECTION_LIMIT = 50
    while True:
        checkout = RawCheckout.get_unprocessed(limit=ROWS_SELECTION_LIMIT)
        for p in checkout:

            msisdn = p.msisdn
            amount = p.amount
            reference_number = p.reference_number


            try:

                access_token = generate_token()
                print(access_token,"access_token")
                api_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

                headers = {"Authorization": "Bearer %s" % access_token}
                request = {
                    "BusinessShortCode": "299533",
                    "Password": PASSWORD,
                    "Timestamp": "20181128132847",
                    "TransactionType": "CustomerPayBillOnline",
                    "Amount": amount,
                    "PartyA": "299533",
                    "PartyB": msisdn,
                    "PhoneNumber": msisdn,
                    "CallBackURL": CallBackURL,
                    "AccountReference": reference_number,
                    "TransactionDesc": "Safari Lotto"
                }


                response = requests.post(api_url, json=request, headers=headers)

                print (response.text)
                p.status=1
                p.reason = "Success. Request accepted for processing"
                p.save()
            except requests.exceptions.Timeout:
                p.reason = "Timeout"
                p.status = 2
                p.save()

            except requests.exceptions.ConnectionError:
                p.reason = "ConnectionError"
                p.status = 2
                p.save()

            except simplejson.scanner.JSONDecodeError:
                p.reason = "JSONDecodeError"
                p.status = 2
                p.save()

            except Exception as e:
                p.reason = str(e)
                p.status = 2
                p.save()

        time.sleep(5)


#runs
run()
