

import requests
from requests.auth import HTTPBasicAuth


def generate_token():

	# consumer_key = 'YFRffqU8Yu914y4v740Os3uZAmGcfFsZ'
	# consumer_secret ='BwkUS6pbjK6XUrmA'
	consumer_key = 'Ylg9fzpD8E57tUf7fJFf8BRX7ReBTlKO'
	consumer_secret = 'Xaplj15j2dppGDIw'
	TOKEN_URL='https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


	r = requests.get(TOKEN_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
	token=r.json()
	print(token)

	return token.get('access_token')


def registerurl():

	access_token = generate_token()
	api_url = "https://api.safaricom.co.ke/mpesa/c2b/v1/registerurl"
	headers = {"Authorization": "Bearer %s" % access_token}
	request = { "ShortCode": "4032353",
	     "ResponseType": "Cancelled",
        "ConfirmationURL": "https://ipn.quickbid.co.ke:7024/ipn/incoming/",
         "ValidationURL": "https://ipn.quickbid.co.ke:7024/ipn/validation/"}

	response = requests.post(api_url, json = request, headers=headers)

	print (response.text)

registerurl()
