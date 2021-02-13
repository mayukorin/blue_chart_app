from django.db import models
from django.utils import timezone
from .siteUser import SiteUser
from .connect import Connect
from .answer_photo import AnswerPhoto


class CommentForConnect(models.Model):

    content = models.TextField(blank=True, null=True)
    comment_user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    connect = models.ForeignKey(
        Connect, on_delete=models.CASCADE, related_name="comments_for_connect"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
