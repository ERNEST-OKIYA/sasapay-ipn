from django.shortcuts import render
from .models import *
from payments.models import Transaction,RawPayouts
from django.http import HttpResponse
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime,date,timedelta


# Create your views here.

class Deposits(View):


	def get(self,request):

		data=Transaction.objects.all()

		return render(request,'admin_portal/deposits.html',{'data':data})


	@method_decorator(login_required,csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(Deposits, self).dispatch(request, *args, **kwargs)

class Payouts(View):


	def get(self,request):

		data=RawPayouts.objects.all()

		return render(request,'admin_portal/payouts.html',{'data':data})


	@method_decorator(login_required,csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(Payouts, self).dispatch(request, *args, **kwargs)

