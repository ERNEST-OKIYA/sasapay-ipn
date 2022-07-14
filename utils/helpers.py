import requests
from requests.auth import HTTPBasicAuth

def generate_token():

	consumer_key = 'yDIxRxTuGs7eORMKxUbwhyCf1fEK6eW4'
	consumer_secret = 'tmwkn1gM7IOUbn3t'
	TOKEN_URL = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

	r = requests.get(TOKEN_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
	token = r.json()

	return token.get('access_token')
