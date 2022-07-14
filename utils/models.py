from django.db import models
import uuid
from django.utils import timezone



# Create your models here.
import uuid

class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_deleted=models.BooleanField(default=False)
    date_time_created=models.DateTimeField(default=timezone.now)
    

    class Meta:
        abstract=True
