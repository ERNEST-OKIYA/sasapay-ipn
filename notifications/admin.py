from django.contrib import admin

# Register your models here.
from .models import *



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass