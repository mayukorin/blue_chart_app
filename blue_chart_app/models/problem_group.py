from django.db import models
from .section import Section


class Problem_group(models.Model):

    name = models.CharField(max_length=50)
    title = models.CharField(max_length=20, default="")
    number = models.IntegerField(default=0, null=True)
    page = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
