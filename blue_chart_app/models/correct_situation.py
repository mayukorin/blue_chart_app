from django.db import models


class CorrectSituation(models.Model):

    situation = models.CharField(null=True, max_length=100)

    def __str__(self):

        return self.situation
