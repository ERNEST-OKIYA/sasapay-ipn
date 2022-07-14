from django.db import models

# Create your models here.
from django.utils import timezone
from django.conf import settings


class Message(models.Model):
    MESSAGE_TYPES={1:'Email',2:'SMS'}
    MESSAGE_STATUS={0:"Un Processed",1:"Processed",2:"Successful",3:"Failed"}
    MESSAGE_PRIORITY={1:"Very Urgent",2:"Urgent",3:"Normal"}


    subject=models.CharField(max_length=100,null=True,help_text="Subject header for emails ") 
    message=models.CharField(max_length=320)
    priority=models.SmallIntegerField(default=3) 
    message_type=models.SmallIntegerField(default=1) 
    
    gateway=models.CharField(max_length=100,help_text="Name of SMS /email gateway")

    message_status=models.SmallIntegerField(default=0) 
    delivery_response=models.CharField(max_length=100,null=True)
    request_id=models.CharField(max_length=300,null=True)
    sender_address=models.CharField(max_length=100,null=True)
    recipient_address=models.CharField(max_length=100)
    template_id=models.CharField(max_length=100,null=True) #name of template to use for emails 
    date_created=models.DateTimeField(default=timezone.now)
    last_updated=models.DateTimeField(default=timezone.now)
    

    @classmethod
    def get_unprocessed(cls): #return messages to be sent
        return cls.objects.filter(message_status=0)

    def is_email(self):
        return self.message_type==1
    def is_sms(self):
        return self.message_type==2

    def done(self):
        #mark this message as processed and successful 
        self.message_status=2
        return self.save()

    def fail(self):
        #mark this message as processed but failed
        self.message_status=3
        return self.save()
        
    @classmethod
    def create_email(cls,message,recipient_address,gateway="gmail",template_id=None,subject=None):

        #if template is provided the message is list of susstitiutions in 
        #the format of "last_name:mogaka" or "last_name:mogaka,first_name:name"
        
        return cls.objects.create(message=message,message_type=1,
                                  sender_address=settings.DEFAULT_FROM_EMAIL,
                                  template_id=template_id,
                                  recipient_address=recipient_address,subject=subject,gateway=gateway)

    @classmethod
    def create_sms(cls,message,recipient_address,gateway='sms'):
       return  cls.objects.create(message=message,message_type=2,recipient_address=recipient_address,gateway=gateway)
                           
    
   
    
    

    