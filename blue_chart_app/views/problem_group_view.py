# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 22:23:19 2020

@author: Mayuko
"""
from django.views import View
from blue_chart_app.models.problem_group import Problem_group
from blue_chart_app.models.section import Section
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


class ProblemGroupListView(LoginRequiredMixin, View):
    def get(self, request, section_id, *args, **kwargs):

        problem_groups = Problem_group.objects.filter(section__id=section_id).order_by(
            "page"
        )
        section = Section.objects.get(pk=section_id)

        return render(
            request,
            "problem_group/list.html",
            {"problem_groups": problem_groups, "section": section},
        )


problem_group_list_view = ProblemGroupListView.as_view()
