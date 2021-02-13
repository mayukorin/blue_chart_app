# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 13:27:13 2020

@author: Mayuko
"""
from django.views import View
from blue_chart_app.models.chapter import Chapter
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


class ChapterListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        chapters = Chapter.objects.all().order_by("subject__id", "number")

        return render(request, "chapter/chapter_list.html", {"chapters": chapters})


chapter_list = ChapterListView.as_view()
