
import requests
from requests.auth import HTTPBasicAuth

class Config:

	BASE_URL='https://api.safaricom.co.ke/'
	CONSUMER_KEY='IEruriKV3M51JHrKfSP4ocMrrwXtuIIh'
	CONSUMER_SECRET='1A6tnmN8pElgNRS0'
	TOKEN_ENDPOINT='oauth/v1/generate?grant_type=client_credentials'
	ACCOUNT_BALANCE_ENDPOINT='mpesa/accountbalance/v1/query'
	REVERSAL_ENDPOINT='mpesa/reversal/v1/request'
	TRANSACTION_STATUS_ENDPOINT='mpesa/transactionstatus/v1/query'
	STK_PUSH_ENDPOINT='mpesa/stkpush/v1/processrequest'
	BusinessShortCode='642086'
	Password='Iwul6327'
	INITIATOR='Joshua'
	Timestamp='20180615121533'
	CallBackURL=''
	TransactionDesc=''
	AccountReference=''
	TransactionType=''
	PASS_KEY='d433b8be80b9e35a722dbb1757d77623ee2448de4bb5fdd36878327d51ff81ac'
	BASE64ENCODED_PASSWORD='NjQyMDg2ZDQzM2I4YmU4MGI5ZTM1YTcyMmRiYjE3NTdkNzc2MjNlZTI0NDhkZTRiYjVmZGQzNjg3ODMyN2Q1MWZmODFhYzIwMTgwNjE1MTIxNTMz'


class Utilities:

	def url(self,endpoint):
		return Config.BASE_URL+endpoint


	def token(self):
		url=self.url(Config.TOKEN_ENDPOINT)
		r = requests.get(url, auth=HTTPBasicAuth(Config.CONSUMER_KEY, Config.CONSUMER_SECRET))
		token=r.json()
		return token.get('access_token')


	def action(self,action):

		pass

	def stk_push(self,msisdn,amount):

		access_token = self.token()
		url = self.url(Config.STK_PUSH_ENDPOINT)
		headers = { "Authorization": "Bearer %s" % access_token }
		request = {
		  "BusinessShortCode":Config.BusinessShortCode,
		  "Password": Config.BASE64ENCODED_PASSWORD,
		  "Timestamp": Config.Timestamp,
		  "TransactionType": "CustomerPayBillOnline",
		  "Amount": amount,
		  "PartyA": msisdn,
		  "PartyB": Config.BusinessShortCode,
		  "PhoneNumber": msisdn,
		  "CallBackURL": "http://138.68.109.245:8000/callback",
		  "AccountReference": "Tuchat",
		  "TransactionDesc": "Test "
		}

		response = requests.post(url, json = request, headers=headers)

		print (response.text)

ut=Utilities()
ut.stk_push('254722912908', 10.00)
