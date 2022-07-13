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
        payouts = RawPayouts.get_unprocessed(limit=ROWS_SELECTION_LIMIT)
        for p in payouts:

            msisdn = p.msisdn
            amount = p.amount
            reference_number = p.reference_number
            short_code = p.short_code
            key = p.key
            merchant=p.merchant


            # try:

            merchant_key=merchant.app_key
            merchant_secret=merchant.app_secret
            merchant_short_code = merchant.b2c_shortcode
            key_text=(msisdn+str(amount)+merchant_key+merchant_secret+reference_number+str(merchant_short_code)).encode('utf-8')
            

            if int(short_code) != merchant_short_code:
                p.status=2
                p.notes= f"Merchant Short Code {short_code} not found"
                p.save()

            elif hashlib.sha256(key_text).hexdigest()!=key:

                p.status=2
                p.notes="Invalid Key"
                p.save()
            else:
                access_token=generate_token()
                print("ACCESS TOKEN",access_token)
                api_url = "https://api.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"

                headers = { "Authorization": "Bearer %s" % access_token }
                request = {
                            "InitiatorName": VARIABLES.get('InitiatorName'),
                            "SecurityCredential": VARIABLES.get('SecurityCredential'),
                            "CommandID":  VARIABLES.get('CommandID'),
                            "Amount": str(amount),
                            "PartyA":  VARIABLES.get('PartyA'),
                            "PartyB": msisdn,
                            "Remarks": reference_number,
                            "QueueTimeOutURL":  VARIABLES.get('QueueTimeOutURL'),
                            "ResultURL":  VARIABLES.get('ResultURL'),
                            "Occasion": " "
                    }
                print(request)

                response = requests.post(api_url, json = request, headers=headers)
                print(response.text,"RESPONSE")
                r=response.json()
                p.status = 1
                p.conversation_id = r.get('ConversationID')
                p.originator_converstation_id = r.get('OriginatorConversationID')
                p.response_code = r.get('ResponseCode')
                p.response_description = r.get('ResponseDescription')
                p.reason = "Request submitted for processing"
                p.save()
            # except requests.exceptions.Timeout:
            #     p.reason = "Timeout"
            #     p.status = 2
            #     p.save()

            # except requests.exceptions.ConnectionError:
            #     p.reason = "ConnectionError"
            #     p.status = 2
            #     p.save()

            # except simplejson.scanner.JSONDecodeError:
            #     p.reason = "JSONDecodeError"
            #     p.status = 2
            #     p.save()

            # except Exception as e:
            #     p.reason = str(e)
            #     p.status = 2
            #     p.save()

        time.sleep(5)


#runs
run()
