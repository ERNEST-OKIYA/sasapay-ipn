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
	ROWS_SELECTION_LIMIT = 500
	TIMEOUT = 3
	PAYOUT_RESULT_URL = 'https://pangabet.com/api/v1/payments/payouts/mpesa/'




	while True:
		#get un processed results for processing

		results = RawPayouts.get_unprocessed_results(
			limit=ROWS_SELECTION_LIMIT)
		for result in results:
			result_status = result.result_status
			result_code = result.result_code
			results = result.results
			transaction_id = result.reference_number
			mpesa_transaction_id = result.transaction_id
			result_description = result.result_description

			payload = {
					'transaction_id':transaction_id,
					'results': results,
					'result_code':result_code,
					'result_description':result_description,
					'mpesa_transaction_id':mpesa_transaction_id
				}

			try:

				r = requests.post(PAYOUT_RESULT_URL, json=payload,timeout=TIMEOUT)

				if r.status_code == 200:
					result.result_status = 1
					result.notes = "Processed"
					result.save()

				else:
					result.result_status = 2
					result.notes = "Error Processing"
					result.save()


			except requests.exceptions.Timeout:
				result.notes = "Timeout"
				result.result_status = 2
				result.save()

			except requests.exceptions.ConnectionError:
				result.notes = "ConnectionError"
				result.results_status = 2
				result.save()

			except simplejson.scanner.JSONDecodeError:
				result.notes = "JSONDecodeError"
				result.result_status = 2
				result.save()

			except Exception as e:
				result.result_status = 2
				result.notes = str(e)
				result.save()



		time.sleep(2)  # wait  seconds before processing again


#runs
run()
