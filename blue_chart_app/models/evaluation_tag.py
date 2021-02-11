from django.db import models
from .type import Type


class EvaluationTag(models.Model):
    
    content = models.CharField(max_length=255, null=True)
    evaluation_type = models.ForeignKey(Type, related_name="evaluation", on_delete=models.CASCADE)
