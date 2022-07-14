
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from .models import DepositRaw
from rest_framework import generics
from utils.views import TransactionalViewMixin
from .serializers import *
from .models import Transaction, PayoutsResponseRaw, RawPayouts, CheckoutResponse, RawCheckout
import threading
import requests
import json
import hashlib


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
		response_xml='''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:c2b="http://cp-
		s.huawei.com/cpsinterface/c2bpayment">
		<soapenv:Header/>
		<soapenv:Body>
		<c2b:C2BPaymentConfirmationResult>C2B Payment Transaction  result '''+transaction_id+''' received.</c2b:C2BPaymentConfirmationResult>
		</soapenv:Body>
		</soapenv:Envelope>'''
		#threading.Thread(target=forward_xml, args=(request.body.decode('utf-8'),'http://138.68.71.27/payments/')).start()
		return HttpResponse(response_xml,content_type="application/xml;charset=utf-8")
	def get(self,request):
		return HttpResponse("Confirm")

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(C2BConfirm, self).dispatch(request, *args, **kwargs)



class C2BValidate(View):
	""" Replies to safaricom on validation of the payment"""
	def post(self,request):
		#data=helpers.process_xml(request.body)
		#Ipn.objects.create(request='C2BValidate',xml=request.body.decode('utf-8'))
		response_xml='''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:c2b="http://cp-
s.huawei.com/cpsinterface/c2bpayment">
<soapenv:Header/>
<soapenv:Body>
<c2b:C2BPaymentValidationResult>
<ResultCode>0</ResultCode>
<ResultDesc>Service processing successful</ResultDesc>
<ThirdPartyTransID>1234560000088888</ThirdPartyTransID>
</c2b:C2BPaymentValidationResult>
</soapenv:Body>
</soapenv:Envelope>'''
		return HttpResponse(response_xml,content_type="application/xml;charset=utf-8")
	def get(self,request):
		return HttpResponse("Validate")

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(C2BValidate, self).dispatch(request, *args, **kwargs)


class B2CQueueTimeout(View):

		def post(self,request):
			#data=helpers.process_xml(request.body)
			#Ipn.objects.create(request='B2CQueueTimeout',xml=request.body.decode('utf-8'))

			response_xml='''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:loc="http://www.csapi.org/schema/timeoutnotification/data/v1_0/local" xmlns:res="http://api-v1.gen.mm.vodafone.com/mminterface/result">
   <soapenv:Header/>
   <soapenv:Body>
	  <loc:notifyQueueTimeoutResponse>
		 <loc:result>
			<res:ResultCode>00000000</res:ResultCode>
			<res:ResultDesc> success</res:ResultDesc>
		 </loc:result>
	  </loc:notifyQueueTimeoutResponse>
   </soapenv:Body>
</soapenv:Envelope>'''

			return HttpResponse(response_xml,content_type="application/xml;charset=utf-8")

		def get(self,request):
				return HttpResponse("B2CQueueTimeout")

		@method_decorator(csrf_exempt)
		def dispatch(self, request, *args, **kwargs):
				return super(B2CQueueTimeout, self).dispatch(request, *args, **kwargs)

class B2CApiResult(View):
	def post(self,request):
		detail=request.body.decode('utf-8')
		PayoutsResponseRaw.record_transaction(detail=detail)

		response_xml='''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:req="http://api-v1.gen.mm.vodafone.com/mminterface/request">
   <soapenv:Header/>
   <soapenv:Body>
	  <req:ResponseMsg><![CDATA[<?xml version="1.0" encoding="UTF-8"?>
<response xmlns="http://api-v1.gen.mm.vodafone.com/mminterface/response">
	<ResponseCode>00000000</ResponseCode>
	<ResponseDesc>success</ResponseDesc>
</response>]]></req:ResponseMsg>
   </soapenv:Body>
</soapenv:Envelope>'''
		return HttpResponse(response_xml,content_type="application/xml;charset=utf-8")

	def get(self,request):
		return HttpResponse("B2CApiResult")

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(B2CApiResult, self).dispatch(request, *args, **kwargs)


class B2CIncoming(View):

	def post(self, request):
		data = json.loads(request.body.decode('utf-8'))
		if RawPayouts.reference_number_exists(data.get('reference_number')):
			return JsonResponse({'error':'A transaction with this reference Number already Exists'})
		else:
			msisdn = data.get('msisdn')
			amount = int(data.get('amount'))
			reference_number = data.get('reference_number')
			key = data.get('key')
			RawPayouts.create_payout(msisdn,amount,reference_number,key)
			return JsonResponse({'status': 'created'})
	def get(self, request):
		return JsonResponse({'status':None})

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(B2CIncoming, self).dispatch(request, *args, **kwargs)


class CheckoutResult(View):
	def post(self, request):
		data = json.loads(request.body.decode('utf-8'))

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




