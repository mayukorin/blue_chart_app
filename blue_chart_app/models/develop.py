from django.db import models
from .problem import Problem


class Develop(models.Model):

    from_problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name="from_develops"
    )
    to_problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name="to_develops"
    )
