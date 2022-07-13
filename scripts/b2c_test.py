import requests
from requests.auth import HTTPBasicAuth
from db import Db #import even when not using.
from utils.resources import VARIABLES
def generate_token():

	# consumer_key = 'YFRffqU8Yu914y4v740Os3uZAmGcfFsZ'
	# consumer_secret ='BwkUS6pbjK6XUrmA'
	consumer_key = 'tkplzofGH8Eikc4BLbn66GqGRgIRmA1x'
	consumer_secret ='jll6W8YGiGGTprqy'
	TOKEN_URL='https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


	r = requests.get(TOKEN_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
	token=r.json()


	return token.get('access_token')

def payout(msisdn,amount):
    access_token=generate_token()

    api_url = "https://api.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
    headers = { "Authorization": "Bearer %s" % access_token }
    request = {
    "InitiatorName": VARIABLES.get('InitiatorName'),
    "SecurityCredential": VARIABLES.get('SecurityCredential'),
    "CommandID":  VARIABLES.get('CommandID'),
    "Amount": amount,
    "PartyA":  VARIABLES.get('PartyA'),
    "PartyB": msisdn,
    "Remarks": " Test Pay",
    "QueueTimeOutURL":  VARIABLES.get('QueueTimeOutURL'),
    "ResultURL":  VARIABLES.get('ResultURL'),
    "Occasion": " "
    }



    response = requests.post(api_url, json = request, headers=headers)

    print (response.text)

# phone_numbers=['254722772222','254722737973','254722435168','254722615420','254722988175','254722912908','254723920149']
phone_numbers=['254722912908',]
for phone_number in phone_numbers:
    print("Sending 10/= to {}".format(phone_number))
    payout(phone_number,10)
#
