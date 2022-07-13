from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import Permission,Group
import random
import string
from .managers import UserManager
from utils.models import UUIDModel

class User(AbstractBaseUser,PermissionsMixin,UUIDModel):
    email=models.EmailField(max_length=200,unique=True)
    password=models.CharField(max_length=300)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    is_superuser=models.BooleanField(default=False)
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.'
        )
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as active. '
    )
    created_by=models.CharField(max_length=50,null=True)
    is_email_verified=models.BooleanField(default=False)
    is_password_changed=models.BooleanField(default=False)
    objects=UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name',]
    
    class Meta:
        verbose_name='user'
        verbose_name_plural='users'
        
    def get_full_name(self):
        return ('%s %s' % (self.first_name, self.last_name)).strip()
    
    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name
  
    def permissions(self):
        #return permsisions in the groups that the user is in 
        return [p.codename for p in Permission.objects.filter(group__user=self)]
    
    @classmethod
    def get_staffs(cls):
        #return all users who are staff
        return cls.objects.filter(is_staff=True,is_deleted=False)

    @classmethod
    def get_all(cls):
        #return all users who are staff
        return cls.objects.filter(is_deleted=False)

    @classmethod
    def get_staff_and_normal(cls):
        #return all users who are staff
        return cls.objects.exclude(is_superuser=True,is_deleted=True)



class Code(models.Model): #used for verifications
    #code reasons
    EMAIL_VERIFICATION=1
    PHONE_NUMBER_VERIFICATION=2

    user=models.ForeignKey(User)
    code=models.CharField(max_length=100)
    reason=models.SmallIntegerField()
    date_created=models.DateTimeField(default=timezone.now)

    @classmethod
    def generate(cls,user,reason):
        #generate general for now
        code=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
        return cls.objects.create(user=user,code=code,reason=reason)
            
    @classmethod
    def is_valid(cls,user,reason,code):
        #verify if code is valid for user action
        try:
            return cls.objects.filter(user=user,reason=reason,code=code).first()
        except:
            return False

    
    
    
    
    
    