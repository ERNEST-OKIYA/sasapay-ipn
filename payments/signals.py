from django.db.models.signals import pre_save
from .models import PayoutsOutgoingRaw

app={'key':'0d50dbd39cbd42a79772df61256e9805',
'secret':'446e778f36e042f0ae48ac4cec5d1865','profile_id':'1710071'}
ujumbe_url='https://api.ujumbe.co.ke/v2/sendSms'

def send_sms(message,phone_number):
        payload={'message':message,'phone_number':phone_number,'profile_id':app.get('profile_id')}
        r=requests.post(ujumbe_url,json=payload,headers={'app-secret':app.get('secret'),'app-key':app.get('key')})

        return r



# def send_notification(sender, **kwargs):

#     is_approved = kwargs['instance'].is_approved
#     amount = kwargs['instance'].amount
#     status = kwargs['instance'].status
#     msisdn = kwargs['instance'].msisdn

#     if amount >=15000:
#         is_approved = 0
#         status=6
#         phone_numbers=['254722218640','254722912908','254729567668',]
#         message=""" {} has made a loan request of KES {}.
#         Please Log in to the portal to approve this Transaction.""".format(msisdn,amount)

#         for phone_number in phone_numbers:
#             send_sms(message, phone_number)


#     else:
#         is_approved=1

# pre_save.connect(send_notification, sender=PayoutsOutgoingRaw)


