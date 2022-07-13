import requests
from requests.auth import HTTPBasicAuth

def generate_token():

	# consumer_key = 'YFRffqU8Yu914y4v740Os3uZAmGcfFsZ'
	# consumer_secret ='BwkUS6pbjK6XUrmA'
	consumer_key = 'tkplzofGH8Eikc4BLbn66GqGRgIRmA1x'
	consumer_secret ='jll6W8YGiGGTprqy'
	TOKEN_URL='https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


	r = requests.get(TOKEN_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
	token=r.json()


	return token.get('access_token')