# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 21:57:48 2020

@author: Mayuko
"""
from django.views import View
from django.shortcuts import render, redirect
from blue_chart_app.forms.siteUserForm import SiteUserRegisterForm, SiteUserLoginForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout


class SiteUserRegisterView(View):
    def get(self, request, *args, **kwargs):

        context = {
            "form": SiteUserRegisterForm(),
        }

        return render(request, "siteUser/register.html", context)

    def post(self, request, *args, **kwargs):

        form = SiteUserRegisterForm(request.POST)

        if not form.is_valid():

            return render(request, "siteUser/register.html", {"form": form})

        siteUser = form.save(commit=False)
        siteUser.set_password(form.cleaned_data["password"])
        siteUser.is_teacher = 1 if form.cleaned_data["is_teacher"] else 0
        siteUser.save()

        messages.success(request, "ユーザ登録が完了しました")

        return redirect("blue_chart_app:siteUser_login")


siteUser_register = SiteUserRegisterView.as_view()


class SiteUserLoginView(View):
    def get(self, request, *args, **kwargs):

        context = {
            "form": SiteUserLoginForm(),
        }

        return render(request, "siteUser/login.html", context)

    def post(self, request, *args, **kwargs):

        form = SiteUserLoginForm(request.POST)

        if not form.is_valid():

            return render(request, "siteUser/login.html", {"form": form})

        site_user = form.get_user()
        site_user.reference_user = site_user
        site_user.save()
        auth_login(request, site_user)

        messages.success(request, "こんにちは" + request.user.username + "さん")

        return redirect("blue_chart_app:answer_all_list")


siteUser_login = SiteUserLoginView.as_view()


class SiteUserLogoutView(View):
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            auth_logout(request)

        messages.success(request, "ログアウトしました")

        return redirect("blue_chart_app:siteUser_login")


siteUser_logout = SiteUserLogoutView.as_view()


class ReferenceUserLoginView(View):
    def get(self, request, *args, **kwargs):

        context = {
            "form": SiteUserLoginForm(),
        }

        return render(request, "siteUser/student/login.html", context)

    def post(self, request, *args, **kwargs):

        form = SiteUserLoginForm(request.POST)

        if not form.is_valid():

            return render(request, "siteUser/student/login.html", {"form": form})

        student = form.get_user()

        request.user.reference_user = student
        request.user.save()

        messages.success(request, student.username + "さんのページへログインしました")

        return redirect("blue_chart_app:answer_all_list")


reference_user_login_view = ReferenceUserLoginView.as_view()


class ReferenceUserLogoutView(View):
    def get(self, request, *args, **kwargs):

        if request.user.reference_user.id != request.user.id:

            reference_user_name = request.user.reference_user.username
            request.user.reference_user = request.user
            request.user.save()

            messages.success(request, reference_user_name + "さんのページをログアウトしました")

        return redirect("blue_chart_app:answer_all_list")


reference_user_logout_view = ReferenceUserLogoutView.as_view()
