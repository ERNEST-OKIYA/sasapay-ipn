from db import Db
import base64
import hashlib
import requests
import time
import simplejson
#import our models
from payments.models import RawPayouts
from utils.helpers import generate_token
from utils.resources import VARIABLES







def run():
    ROWS_SELECTION_LIMIT = 50
    while True:
        payouts = RawPayouts.get_unprocessed_results(limit=ROWS_SELECTION_LIMIT)
        for p in payouts:

            msisdn = p.msisdn
            amount = p.amount
            reference_number = p.reference_number
            result_code = p.result_code
            merchant = p.merchant
            mpesa_code = p.mpesa_code
            url = merchant.payout_results_ipn_url
            result_description = p.result_description



            try:
                

                payload = {
                            'msisdn':msisdn,
                            'amount':amount,
                            'reference_number':reference_number,
                            'result_code':result_code,
                            'mpesa_code':mpesa_code,
                            'result_description': result_description,
                          }

                r = requests.post(url,json=payload,timeout=30,verify=False)
                print(r.text)
                rv = r.json()
               
                if r.status_code == requests.codes.ok:
                    p.tp_results_notes = 'Results Accepted'
                    
                else:
                    
                    p.tp_results_notes = 'Results Callback errored'
                p.third_party_response_sent=1
                p.save()



            except requests.exceptions.Timeout as exc:

                p.third_party_response_sent = 2
                p.tp_results_notes = str(exc)
                p.save()

            except requests.exceptions.ConnectionError as exc:

                p.third_party_response_sent = 2
                p.tp_results_notes = str(exc)
                p.save()

            except simplejson.scanner.JSONDecodeError as exc:

                p.third_party_response_sent = 2
                p.tp_results_notes = str(exc)
                p.save()

            except Exception as exc:

                p.third_party_response_sent = 2
                p.tp_results_notes = str(exc)
                p.save()

        time.sleep(5)


#runs
run()
