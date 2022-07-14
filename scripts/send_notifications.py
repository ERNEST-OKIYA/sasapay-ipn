from db import Db
from django.core.mail import send_mail
from notifications.models import Message
import time

def run():
    while True:
        #get messages to send 
        messages=Message.get_unprocessed()        
        for m in messages:
            if m.is_email():
             
                #send via mail 
                subject=m.subject if m.subject else 'Email Subject '
                try:
                    send_mail(subject,m.message,m.sender_address,[m.recipient_address],fail_silently=False,)
                    m.done() #mark as sent and successful 
                except:
                    #@TODO know how to process this 
                    m.fail() #mark as sent but failed
                
            
            elif m.is_sms():
                #send sms here 
                #@TODO implement this in your way 
                pass 
            
        time.sleep(2) #wait 2 seconds before sending again 

#runs
run()
