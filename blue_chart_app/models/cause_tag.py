from django.db import models
from .type import Type


class CauseTag(models.Model):

    content = models.CharField(max_length=255, null=True)
    cause_type = models.ForeignKey(
        Type, related_name="cause", on_delete=models.CASCADE, null=True
    )
