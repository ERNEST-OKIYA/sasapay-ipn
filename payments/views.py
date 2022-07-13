
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
import base64
import hashlib
from ipware import get_client_ip

from .models import DepositRaw

from rest_framework import generics
from merchants.models import Merchant
from utils.views import TransactionalViewMixin
from .serializers import *
from .models import Transaction, PayoutsResponseRaw, RawPayouts, CheckoutResponse, RawCheckout
from utils.permissions import WhitelistPermission

import threading
import requests
import json
import requests
import hashlib
from django.db import IntegrityError

def validate_payment(payload):
    try:
        url = 'https://quickbid.co.ke/ipn/validate/'
        r = requests.post(url=url,json=payload,timeout=5)
        rv = r.json()
    except:
        rv = {'accepted':True}

    return rv


class TransactionList(TransactionalViewMixin,generics.ListAPIView):
    """ this list transactions """

    serializer_class=TransactionSerializer

    def perform_create(self,serializer):
        #do not implement
        pass

    def get_queryset(self):
        return Transaction.objects.all()


class C2BConfirm(View):
    def post(self,request):
        detail=request.body.decode('utf-8')
        data=json.loads(detail)
        dr=DepositRaw.record_deposit(detail=detail)
        transaction_type=data.get('TransactionType')
        transaction_id=data.get('TransID')
        transaction_timestamp=data.get('TransTime')
        amount=data.get('TransAmount')
        business_shortcode=data.get('BusinessShortCode')
        bill_reference_number=data.get('BillRefNumber')
        msisdn=data.get('MSISDN')
        first_name=data.get('FirstName')
        middle_name=data.get('MiddleName')
        last_name=data.get('LastName')
        organasation_account_balance=data.get('OrgAccountBalance')

        Transaction.insert_deposit(transaction_type,transaction_id,transaction_timestamp,\
                       amount,business_shortcode,\
                       bill_reference_number,msisdn,\
                       first_name,middle_name,last_name,\
                       organasation_account_balance)
        
        
        response={'ResultCode':0,'ResultDesc':'Success'}
        return JsonResponse(response)
    def get(self,request):
        return HttpResponse("Confirm")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(C2BConfirm, self).dispatch(request, *args, **kwargs)



class C2BValidate(View):
    """ Replies to safaricom on validation of the payment"""
    def post(self,request):
        detail=request.body.decode('utf-8')
        data=json.loads(detail)
        res = validate_payment(data)
        if res.get('accepted'):
            response={'ResultCode':0,'ResultDesc':'Success'}
        else:
            response={'ResultCode':1,'ResultDesc':'Failed'}

        return JsonResponse(response)
    def get(self,request):
        return HttpResponse("Validate")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(C2BValidate, self).dispatch(request, *args, **kwargs)


class B2CQueueTimeout(View):

        def post(self,request):
            response={'ResultCode':0,'ResultDesc':'Success'}

            return JsonResponse(response)

        def get(self,request):
                return HttpResponse("B2CQueueTimeout")

        @method_decorator(csrf_exempt)
        def dispatch(self, request, *args, **kwargs):
                return super(B2CQueueTimeout, self).dispatch(request, *args, **kwargs)

class B2CApiResult(View):
    def post(self,request):
        detail=request.body.decode('utf-8')
        PayoutsResponseRaw.record_transaction(detail=detail)

        response={'ResultCode':0,'ResultDesc':'Success'}
        return JsonResponse(response)

    def get(self,request):
        return HttpResponse("B2CApiResult")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(B2CApiResult, self).dispatch(request, *args, **kwargs)


class B2CIncoming(View):

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        msisdn = data.get('msisdn')
        amount = int(data.get('amount'))
        reference_number = data.get('ref_no')
        key = data.get('key')
        short_code = data.get('short_code')
        is_valid = self.validate(short_code,request)
        if is_valid:
            obj,created = RawPayouts.create_payout(msisdn,amount,reference_number,key,short_code)
            if not created:
                response = {'status': 'Payout Already Exists'}
                return JsonResponse(response,status=403)
            else:
                response = {'status': 'created'}
                return JsonResponse(response)
        else:
            return JsonResponse({'status':'Forbidden'},status=403)
    def get(self, request):
        return JsonResponse({'status':None})

    def validate(self,short_code,request):
        try:
            merchant = Merchant.get_merchant_by_b2c_shortcode(short_code)
            ip, is_routable = get_client_ip(request)
            if ip is None:
                return False
            else:
                if is_routable and ip == merchant.public_ip:
                    return True

                else:
                    return False
        except (Merchant.DoesNotExist,Exception,IntegrityError):
            return False


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    


class CheckoutResult(View):
    def post(self, request):
        data = request.body.decode('utf-8')

        CheckoutResponse.objects.create(response=data)
        return JsonResponse({'status': 'created'})

    def get(self, request):
        return JsonResponse({'status': None})

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CheckoutResult, self).dispatch(request, *args, **kwargs)


class IncomingCheckouts(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        msisdn=data.get('msisdn')
        amount = int(data.get('amount'))
        reference_number = data.get('reference_number')
        RawCheckout.objects.create(msisdn=msisdn,amount=amount,reference_number=reference_number)
        return JsonResponse({'status': 'created'})

    def get(self, request):
        return JsonResponse({'status': None})

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(IncomingCheckouts, self).dispatch(request, *args, **kwargs)




