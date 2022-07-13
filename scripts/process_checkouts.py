from db import Db
import base64
import hashlib
import requests
from requests.auth import HTTPBasicAuth
import time
import simplejson
#import our models
from payments.models import RawCheckout


CallBackURL = 'http://46.101.58.107:8060/ipn/checkout-response/'
PASSWORD = 'NTIzMzg4YWRlNjIzNzMxMGI0ZmJmMjBiOTdmNDJkMjA0MWZmYmNkMDUxZWQyOGE2Y2UzYzQ5YmU3YjIwMTQxNTcwYjMxNTIwMTkwMjI4MTMyODQ3'

CONSUMER_KEY = '2YyhGASsOG6za7QN7UAZeAIJn9AOocNT'
CONSUMER_SECRET = 'GAdNPGYCrzDg6nRU'
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
                    "BusinessShortCode": "523388",
                    "Password": PASSWORD,
                    "Timestamp": "20190228132847",
                    "TransactionType": "CustomerPayBillOnline",
                    "Amount": amount,
                    "PartyA": "523388",
                    "PartyB": msisdn,
                    "PhoneNumber": msisdn,
                    "CallBackURL": CallBackURL,
                    "AccountReference": reference_number,
                    "TransactionDesc": "Chomoa Hela"
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

        time.sleep(1)


#runs
run()
