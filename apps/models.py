from django.db import models

# Create your models here.
from django.db import models
from users.models import User
import uuid


def gen_uuid():
    return uuid.uuid4().hex

class App(models.Model):
    name=models.CharField(max_length=100, unique=True)
    b2c_shortcode=models.IntegerField(unique=True)
    c2b_shortcode=models.IntegerField(unique=True)

    charges_paid_account_balance=models.DecimalField(max_digits=12,decimal_places=2,default=0.0)
    utility_account_balance=models.DecimalField(max_digits=12,decimal_places=2,default=0.0)
    working_account_balance=models.DecimalField(max_digits=12,decimal_places=2,default=0.0)

    ipn_url=models.URLField()
    name=models.CharField(max_length=100, unique=True)
    user=models.OneToOneField(User)
    app_key=models.CharField(max_length=100,default=gen_uuid)
    app_secret=models.CharField(max_length=100,default=gen_uuid)


