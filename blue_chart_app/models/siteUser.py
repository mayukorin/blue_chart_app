from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class SiteUser(AbstractUser):
    
    is_teacher = models.IntegerField(default=0)
    reference_user = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, default=None
    )
