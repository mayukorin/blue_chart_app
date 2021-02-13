from django.db import models
from .problem_group import Problem_group


class Problem(models.Model):

    name = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
    page = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)
    problem_group = models.ForeignKey(
        Problem_group, on_delete=models.CASCADE, related_name="problems"
    )

    def __str__(self):

        return self.name
