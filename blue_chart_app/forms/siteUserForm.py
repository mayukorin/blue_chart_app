# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 22:13:00 2020

@author: Mayuko
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from django.core.exceptions import ObjectDoesNotExist
from blue_chart_app.models.siteUser import SiteUser


class SiteUserRegisterForm(forms.ModelForm):
    class Meta:
        model = SiteUser

        fields = ("username", "password")

        widgets = {
            "password": forms.PasswordInput(attrs={"placeholder": "パスワード"}),
            "username": forms.TextInput(attrs={"placeholder": "名前"}),
        }

        labels = {
            "password": "パスワード",
            "username": "名前",
        }

    is_teacher = forms.BooleanField(required=False)


class SiteUserLoginForm(forms.Form):

    username = UsernameField(label="ユーザ名", max_length=255,)

    password = forms.CharField(
        label="パスワード", strip=False, widget=forms.PasswordInput(render_value=True),
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean_username(self):

        username = self.cleaned_data["username"]

        if len(username) < 3:
            raise forms.ValidationError(
                "%(min_length)s文字以上で入力してください", params={"min_length": 3}
            )

        return username

    def clean_password(self):

        password = self.cleaned_data["password"]

        return password

    def clean(self):

        username = self.cleaned_data.get("username")

        password = self.cleaned_data.get("password")

        try:

            site_user = get_user_model().objects.get(username=username)

        except ObjectDoesNotExist:

            raise forms.ValidationError("正しい名前とパスワードを入力してください")

        if not site_user.check_password(password):
            raise forms.ValidationError("正しい名前とパスワードを入力してください")

        self.user_cache = site_user

    def get_user(self):
        return self.user_cache
