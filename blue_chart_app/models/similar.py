from django.db import models
from .problem import Problem


class Similar(models.Model):

    from_problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="from_similars",
        null=True,
        default=None,
    )
    to_problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="to_similars",
        null=True,
        default=None,
    )
