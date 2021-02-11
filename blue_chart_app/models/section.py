from django.db import models
from .chapter import Chapter


class Section(models.Model):

    name = models.CharField(max_length=20)
    number = models.IntegerField(default=0)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
