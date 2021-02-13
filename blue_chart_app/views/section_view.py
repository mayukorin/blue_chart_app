# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 00:46:28 2020

@author: Mayuko
"""
from django.views import View
from blue_chart_app.models.section import Section
from blue_chart_app.models.chapter import Chapter
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


class SectionListView(LoginRequiredMixin, View):
    def get(self, request, chapter_id, *args, **kwargs):

        sections = Section.objects.filter(chapter__id=chapter_id).order_by("number")
        chapter = Chapter.objects.get(pk=chapter_id)

        return render(
            request, "section/list.html", {"sections": sections, "chapter": chapter}
        )


section_list_view = SectionListView.as_view()
