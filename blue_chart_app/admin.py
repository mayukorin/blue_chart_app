from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from blue_chart_app.models.siteUser import SiteUser
from blue_chart_app.models.subject import Subject
from blue_chart_app.models.chapter import Chapter
from blue_chart_app.models.section import Section
from blue_chart_app.models.problem_group import Problem_group
from blue_chart_app.models.problem import Problem
from blue_chart_app.models.similar import Similar
from blue_chart_app.models.develop import Develop
from blue_chart_app.models.answer_photo import AnswerPhoto
from blue_chart_app.models.answer import Answer
from blue_chart_app.models.correct_situation import CorrectSituation
from blue_chart_app.models.type import Type
from blue_chart_app.models.evaluation_tag import EvaluationTag
from blue_chart_app.models.evaluate import Evaluate
from blue_chart_app.models.cause_tag import CauseTag
from blue_chart_app.models.connect import Connect
from blue_chart_app.models.latest_connect import LatestConnect
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = SiteUser
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('is_teacher',)}),)
    list_display = ['username', 'email', 'is_teacher']
 
 
admin.site.register(SiteUser, CustomUserAdmin)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Section)
admin.site.register(Problem_group)
admin.site.register(Problem)
admin.site.register(Similar)
admin.site.register(Develop)
admin.site.register(AnswerPhoto)
admin.site.register(Answer)
admin.site.register(CorrectSituation)
admin.site.register(Type)
admin.site.register(EvaluationTag)
admin.site.register(Evaluate)
admin.site.register(CauseTag)
admin.site.register(Connect)
admin.site.register(LatestConnect)
# Register your models here.
