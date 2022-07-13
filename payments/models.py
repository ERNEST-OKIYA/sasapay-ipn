from django.db import models
from django.utils import timezone

# Create your models here.

import uuid

from merchants.models import Merchant
from django.db.models import Q
import requests
from users.models import User



#remove this after migrations

def generate_transaction_id():
    return uuid.uuid4().int

class Transact(object):
    """ to be injerited """

    #transaction status
    STATUS_INITIAL=0
    STATUS_RETRY=3
    STATUS_PROCESSED=1
    STATUS_FAILED=2 #used mostly in c2b call to client app

    MAX_CLIENT_API_CALLS=3 #maxim number of times to call customer api, before marking row as failed
    MAX_CLIENT_API_CALL_TIMEOUT=5 #number of seconds for timeout URL for customer client api call

    @staticmethod
    def generate_transaction_id():
        return uuid.uuid4().int



class DepositRaw(Transact,models.Model):
    """Store and process incoming transactions from mpesa . on deposits  """
    detail=models.TextField(null=True,blank=True)
    status=models.IntegerField(default=Transact.STATUS_INITIAL)
    reason=models.CharField(max_length=100,null=True)
    api_calls=models.IntegerField(default=0)
    transaction_id=models.CharField(max_length=200,default=generate_transaction_id)
    date_time_created=models.DateTimeField(default=timezone.now)

    @classmethod
    def record_deposit(cls,detail):
        return cls.objects.create(detail=detail)

    @classmethod
    def get_unprocessed(cls,limit):
        return cls.objects.filter(status=Transact.STATUS_INITIAL).order_by('id')[:limit]



class Transaction(models.Model):


    transaction_type=models.CharField(max_length=100)
    transaction_id=models.CharField(max_length=50,null=True)
    transaction_timestamp=models.CharField(max_length=100)
    amount=models.DecimalField(max_digits=12,decimal_places=2,default=0.0)
    business_shortcode=models.IntegerField()
    bill_reference_number=models.CharField(max_length=100,null=True)
    msisdn=models.CharField(max_length=20)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    middle_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    organasation_account_balance=models.DecimalField(max_digits=12,decimal_places=2,null=True)
    date_time_created=models.DateTimeField(default=timezone.now)


    @classmethod
    def insert_deposit(cls,transaction_type,transaction_id,transaction_timestamp,\
                       amount,business_shortcode,\
                       bill_reference_number,msisdn,\
                       first_name,middle_name,last_name,\
                       organasation_account_balance):
        return cls.objects.create(transaction_type=transaction_type,\
                                  transaction_id=transaction_id,
                                 transaction_timestamp=transaction_timestamp,\
                                 amount=amount,business_shortcode=business_shortcode,
                                  bill_reference_number=bill_reference_number,\
                                  msisdn=msisdn,
                                  first_name=first_name,middle_name=middle_name,\
                                  last_name=last_name,\
                                  organasation_account_balance=organasation_account_balance)





class WhiteListIP(models.Model):
    computer_name=models.CharField(max_length=100)
    ip_addr=models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

class PayoutsResponseRaw(models.Model,Transact):
    detail = models.TextField()
    status = models.IntegerField(default=Transact.STATUS_INITIAL)
    reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def record_transaction(cls,detail):
        return cls.objects.create(detail=detail)

    @classmethod
    def get_unprocessed(cls,limit):
        return cls.objects.filter(status=Transact.STATUS_INITIAL).order_by('id')[:limit]


class PayoutsResponseProcessed(models.Model):
    TransactionReceipt = models.CharField(max_length=100)
    TransactionAmount = models.IntegerField()
    B2CWorkingAccountAvailableFunds = models.DecimalField(max_digits=7,decimal_places=2)
    B2CUtilityAccountAvailableFunds = models.DecimalField(max_digits=10,decimal_places=2)
    TransactionCompletedDateTime = models.CharField(max_length=20)
    ReceiverPartyPublicName = models.CharField(max_length=100)
    B2CChargesPaidAccountAvailableFunds = models.DecimalField(max_digits=10,decimal_places=2)
    B2CRecipientIsRegisteredCustomer = models.CharField(max_length=10,default='Y')
    created_at = models.DateTimeField(default=timezone.now)

class B2CErrors(models.Model):
    ResultType = models.IntegerField()
    ResultCode = models.IntegerField()
    ResultDesc = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

class RawPayouts(Transact,models.Model):

    """Stores data from third party to be processesed when sending messages"""


    status = models.IntegerField(default=Transact.STATUS_INITIAL)
    reason = models.TextField(null=True,blank=True)
    msisdn = models.CharField(max_length=20)
    amount = models.IntegerField()
    reference_number = models.CharField(max_length=200,unique=True)
    merchant = models.ForeignKey(Merchant)
    short_code = models.CharField(max_length=10)
    key = models.TextField()
    is_validated = models.IntegerField(default=0)
    conversation_id = models.CharField(max_length=200,blank=True,null=True)
    originator_converstation_id = models.CharField(max_length=200,blank=True,null=True)
    response_description = models.TextField(max_length=100,blank=True,null=True)
    result_code = models.CharField(max_length=100,null=True,blank=True)
    result_description = models.TextField(blank=True, null=True)
    mpesa_code = models.CharField(max_length=10,null=True,blank=True)
    third_party_response_sent = models.IntegerField(default=Transact.STATUS_INITIAL)
    notes = models.TextField(blank=True, null=True)
    tp_results_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def create_payout(cls,msisdn,amount,reference_number,key,short_code):
        merchant=Merchant.objects.get(b2c_shortcode=short_code)
        obj,created = cls.objects.get_or_create(reference_number=reference_number,
        defaults=dict(msisdn=msisdn,amount=int(amount),
        reference_number=reference_number,
        merchant=merchant,key=key,short_code=short_code
        ))
        return (obj,created)

    @classmethod
    def get_unprocessed(cls,limit):
        return cls.objects.filter(status=Transact.STATUS_INITIAL).order_by('id')[:limit]

    @classmethod
    def get_unprocessed_results(cls,limit):
        return cls.objects.filter(status=1).filter(third_party_response_sent=Transact.STATUS_INITIAL)\
            .exclude(result_description__isnull=True).order_by('id')[:limit]

    @classmethod
    def update_payout(cls, result_code, result_description, originator_converstation_id,mpesa_code):
        return cls.objects.filter(originator_converstation_id=originator_converstation_id)\
        .update(result_code=result_code,result_description=result_description,mpesa_code=mpesa_code)


class RawCheckout(Transact,models.Model):
    amount = models.IntegerField()
    msisdn = models.CharField(max_length=13)
    status = models.IntegerField(default=Transact.STATUS_INITIAL)
    reference_number = models.CharField(max_length=50)
    reason = models.CharField(max_length=200,blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def get_unprocessed(cls, limit):
        return cls.objects.filter(status=Transact.STATUS_INITIAL).order_by('id')[:limit]

class CheckoutResponse(Transact,models.Model):
    response = models.TextField()
    status = models.IntegerField(default=Transact.STATUS_INITIAL)
    created_at = models.DateTimeField(default=timezone.now)

class Balance(models.Model):
    working_balance = models.CharField(max_length=20, blank=True,null=True)
    utility_balance = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def update_balance(cls, utility_balance,working_balance):
        return cls.objects.filter(pk=1).update(utility_balance=utility_balance,working_balance=working_balance)



