from django.db import models
from .evaluate import Evaluate
from .siteUser import SiteUser
from django.utils import timezone


class CommentForEvaluate(models.Model):

    content = models.TextField(blank=True, null=True)
    evaluate = models.ForeignKey(
        Evaluate, on_delete=models.CASCADE, related_name="comments_for_evaluate"
    )
    comment_user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
