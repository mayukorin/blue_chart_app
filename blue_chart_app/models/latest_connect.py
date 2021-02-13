from django.db import models
from .problem import Problem
from .cause_tag import CauseTag
from .siteUser import SiteUser
from .connect import Connect
from django.db.models import Count


class LatestConnect(models.Model):
    
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    cause_tag = models.ForeignKey(CauseTag, related_name="latest_connects", on_delete=models.CASCADE)
    solve_user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    connect_model = models.OneToOneField(Connect, on_delete=models.SET_NULL, null=True)
    
    def get_count_of_not_overcome_answer(self):

        count_of_not_overcome_answer = Connect.objects.select_related("latest_connect").filter(is_overcome=False).filter(latest_connect=self).count()

        return count_of_not_overcome_answer
