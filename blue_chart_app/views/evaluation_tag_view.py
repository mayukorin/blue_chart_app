# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 16:19:44 2021

@author: Mayuko
"""


from django.views import View
from blue_chart_app.forms.evaluationTagForm import EvaluationTagRegisterForm
from django.shortcuts import render, redirect
from blue_chart_app.models.problem import Problem
from blue_chart_app.models.answer_photo import AnswerPhoto
from blue_chart_app.models.answer import Answer
from blue_chart_app.models.evaluate import Evaluate
from blue_chart_app.models.comment_for_evaluate import CommentForEvaluate
from blue_chart_app.models.evaluation_tag import EvaluationTag
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from blue_chart_app.forms.evaluationTagForm import EvaluationTagSearchForm
from django.db.models import Count


class EvaluationTagSuggestView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        keyword = request.GET.get("keyword")

        if keyword:

            evaluation_tag_list = [
                {"pk": ev.pk, "content": ev.content, "type_id": ev.evaluation_type.id}
                for ev in EvaluationTag.objects.filter(content__icontains=keyword)
            ]

        else:

            evaluation_tag_list = []

        return JsonResponse({"object_list": evaluation_tag_list})


evaluation_tag_suggest_view = EvaluationTagSuggestView.as_view()


class EvaluatinoTagSearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        form = EvaluationTagSearchForm()

        return render(request, "evaluation_tag/search.html", {"form": form})

    def post(self, request, *args, **kwargs):

        form = EvaluationTagSearchForm(request.POST)

        if not form.is_valid():

            return render(request, "evaluation_tag/search.html", {"form": form})

        if form.cleaned_data["content_keyword"] != "":
            problems_for_evaluation_keyword = (
                Evaluate.objects.select_related()
                .filter(good_flag=1)
                .filter(
                    evaluation_tag__content__icontains=form.cleaned_data[
                        "content_keyword"
                    ]
                )
                .values(
                    "evaluation_tag",
                    "problem",
                    "problem__name",
                    "evaluation_tag__evaluation_type__id",
                    "evaluation_tag__content",
                )
                .annotate(total=Count("evaluation_tag"))
            )
        else:
            problems_for_evaluation_keyword = (
                Evaluate.objects.select_related()
                .filter(good_flag=1)
                .values(
                    "evaluation_tag",
                    "problem",
                    "problem__name",
                    "evaluation_tag__evaluation_type__id",
                    "evaluation_tag__content",
                )
                .annotate(total=Count("evaluation_tag"))
            )

        for pfek in problems_for_evaluation_keyword:

            pfek["bad_flag_count"] = (
                Evaluate.objects.filter(good_flag=0)
                .filter(evaluation_tag__id=pfek["evaluation_tag"])
                .filter(problem__id=pfek["problem"])
                .count()
            )

        context = {
            "problems_for_evaluation_keyword": problems_for_evaluation_keyword,
            "keyword": form.cleaned_data["content_keyword"],
        }
        return render(request, "evaluation_tag/result.html", context)


evaluation_tag_search_view = EvaluatinoTagSearchView.as_view()
