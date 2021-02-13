from django.db import models
from django.utils import timezone
from .siteUser import SiteUser
from .answer import Answer


class CommentForAnswer(models.Model):

    content = models.TextField(blank=True, null=True)
    comment_user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, null=True, related_name="comments_for_answer"
    )
