from django.db import models
from .subject import Subject


class Chapter(models.Model):

    name = models.CharField(max_length=20)
    number = models.IntegerField(default=0)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
