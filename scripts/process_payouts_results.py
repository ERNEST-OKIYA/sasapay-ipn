import requests
import time
import simplejson

import xml.etree.ElementTree as ET
import decimal

import sys

import json

from db import Db  # import even when not using.

from django.conf import settings
from django.utils import timezone
from django.db import transaction

#import our models
from payments.models import PayoutsResponseRaw, Transaction, RawPayouts,Balance

from merchants.models import Merchant



def run():
	ROWS_SELECTION_LIMIT = 50
	def is_balance(obj):
		balance_values=['B2CUtilityAccountAvailableFunds', 'B2CWorkingAccountAvailableFunds']
		return obj['Key'] in balance_values



	while True:
		#get un processed results for processing

		results = PayoutsResponseRaw.get_unprocessed(
			limit=ROWS_SELECTION_LIMIT)
		for result in results:
			detail = json.loads(result.detail)
			print(detail)

			try:
				result_code = detail.get('Result')['ResultCode']

				originator_converstation_id = detail.get('Result')[
					'OriginatorConversationID']
				result_description = detail.get('Result')[
					'ResultDesc']
				transaction_id = detail.get('Result')['TransactionID']
				if str(result_code) =='0':
					result_parameters = detail['Result']['ResultParameters']['ResultParameter']
					result_parameters = result_parameters
					f = (obj for obj in result_parameters if is_balance(obj))

					balances ={}
					for ob in f:
						balances[ob["Key"]] = ob['Value']
					utility_balance = balances['B2CUtilityAccountAvailableFunds']
					working_balance = balances['B2CWorkingAccountAvailableFunds']

					bal=Balance.update_balance(utility_balance,working_balance)
				else:
					pass
				up=RawPayouts.update_payout(result_code,result_description,originator_converstation_id,transaction_id,detail)
				result.status = 1
				result.save()
			except Exception as e:
				print(e,"exception")
				result.status =2
				result.reason = str(e)
				result.save()


		time.sleep(1)  # wait  seconds before processing again


#runs
run()
