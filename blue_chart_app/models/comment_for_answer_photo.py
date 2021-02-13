from django.db import models
from django.utils import timezone
from .siteUser import SiteUser
from .answer import Answer
from .answer_photo import AnswerPhoto


class CommentForAnswerPhoto(models.Model):
    
    content = models.TextField(blank=True, null=True)
    comment_user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    answer_photo = models.ForeignKey(AnswerPhoto, on_delete=models.PROTECT, null=True, related_name='comments_for_answer_photo')

