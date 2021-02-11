from django.db import models
from .cause_tag import CauseTag
from .siteUser import SiteUser


class Connect(models.Model):

    answer = models.ForeignKey(
        "Answer", related_name="connects", on_delete=models.CASCADE
    )
    cause_tag = models.ForeignKey(
        CauseTag, related_name="connects", on_delete=models.CASCADE
    )
    connect_user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    latest_connect = models.ForeignKey(
        "LatestConnect", on_delete=models.CASCADE, null=True
    )
    is_overcome = models.BooleanField(null=True)
