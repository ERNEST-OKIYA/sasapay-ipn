from django.db import models

# Create your models here.
from django.db import models
from users.models import User
import uuid


def gen_uuid():
    return uuid.uuid4().hex

class Merchant(models.Model):
    name=models.CharField(max_length=100, unique=True)
    b2c_shortcode=models.IntegerField(unique=True)
    c2b_shortcode=models.IntegerField(unique=True)

    organisation_account_balance=models.DecimalField(max_digits=12,decimal_places=2,default=0.0)
    charges_paid_account_balance=models.DecimalField(max_digits=12,decimal_places=2,default=0.0)
    utility_account_balance=models.DecimalField(max_digits=12,decimal_places=2,default=0.0)
    working_account_balance=models.DecimalField(max_digits=12,decimal_places=2,default=0.0)

    deposits_ipn_url=models.URLField()
    payout_results_ipn_url=models.URLField(null=True,blank=True)
    public_ip = models.CharField(max_length=20,null=True)
    user=models.OneToOneField(User,on_delete=models.DO_NOTHING)
    app_key=models.CharField(max_length=100,default=gen_uuid)
    app_secret=models.CharField(max_length=100,default=gen_uuid)

    is_deleted=models.BooleanField(default=False)


    def user_full_name(self):
        return self.user.get_full_name()


    @classmethod
    def get_merchant_by_c2b_shortcode(cls,shortcode):
        try:
            return cls.objects.get(c2b_shortcode=shortcode,is_deleted=False)
        except:
            #not found
            return None


    @classmethod
    def get_merchant_by_b2c_shortcode(cls,shortcode):
        try:
            return cls.objects.get(b2c_shortcode=shortcode,is_deleted=False)
        except:
            return None



    @classmethod
    def get_user(cls,app_key,app_secret):
        try:
            return cls.objects.get(app_key=app_key,app_secret=app_secret).user
        except User.DoesNotExist:
            return None
        except Exception as e:
            return None
        





