import requests
import time
import simplejson

import xml.etree.ElementTree as ET
import decimal

import sys

import json

from db import Db #import even when not using.

from django.conf import settings
from django.utils import timezone
from django.db import transaction

#import our models
from payments.models import DepositRaw,Transaction

from merchants.models import Merchant


#sample received xml for deposit is as below

"""
{
            "TransactionType": "Pay Bill",
            "TransID": "MK92RM2ZWY",
            "TransTime": "20181109092506",
            "TransAmount": "2.00",
            "BusinessShortCode": "299533",
            "BillRefNumber": "test ",
            "InvoiceNumber": "",
            "OrgAccountBalance": "182.00",
            "ThirdPartyTransID": "",
            "MSISDN": "254722912908",
            "FirstName": "ABUGA",
            "MiddleName": "J",
            "LastName": "BICHANG'A"
        }


"""

def run():
    ROWS_SELECTION_LIMIT=50
    RESPONSE_ACCEPTED='ACCEPTED'
    RESPONSE_FAILED='FAILED'




    while True:
        #get un processed deposits for processing

        deposits=DepositRaw.get_unprocessed(limit=ROWS_SELECTION_LIMIT)
        for deposit in deposits:
            detail=json.loads(deposit.detail)
            api_calls=deposit.api_calls

            try:
                BusinessShortCode = detail.get('BusinessShortCode')
                deposits_ipn_url=Merchant.objects.get(c2b_shortcode=BusinessShortCode).deposits_ipn_url

                response=requests.post(deposits_ipn_url,json=detail,verify=False,timeout=deposit.MAX_CLIENT_API_CALL_TIMEOUT)
                response_data=response.json()
                response_status=response_data.get('status',RESPONSE_FAILED)
                deposit.reason=response_status
                deposit.status=1
                deposit.api_calls = 1
                deposit.save()
            except requests.exceptions.Timeout:
                response_status=RESPONSE_FAILED
                status_reason='Timeout'
                deposit.reason = status_reason
                deposit.status = 0
                deposit.save()

            except requests.exceptions.ConnectionError:
                #url is dead
                response_status=RESPONSE_FAILED
                status_reason='ConnectionError'
                deposit.reason = status_reason
                deposit.status = 0
                deposit.save()

            except simplejson.scanner.JSONDecodeError:
                response_status=RESPONSE_FAILED
                status_reason='JSONDecodeError'
                deposit.reason = status_reason
                deposit.status = 0
                deposit.save()


        time.sleep(1) #wait  seconds before processing again



#runs
run()




