# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 15:18:41 2021

@author: Mayuko
"""


from django import forms
from blue_chart_app.models.cause_tag import CauseTag
from blue_chart_app.models.type import Type
from blue_chart_app.models.connect import Connect
from django.core.exceptions import ObjectDoesNotExist


class CauseTagRegisterForm(forms.ModelForm):
    class Meta:
        model = CauseTag
        fields = ("content", "cause_type")

        labels = {
            "content": "原因タグの内容",
            "cause_type": "原因タグのタイプ",
        }

        widgets = {
            "content": forms.TextInput(attrs={"class": "form-control"}),
            "evaluation_type": forms.Select(attrs={"class": "form-control"}),
        }

    cause_type = forms.ModelChoiceField(
        queryset=Type.objects.all().order_by("id"),
        empty_label=None,
        label="原因タグのタイプ",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    comment_for_connect = forms.CharField(
        label="コメント（任意）",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )

    def __init__(self, answer_id=0, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields["content"].required = False
        self.cause_tag_cache = None
        self.answer_id = answer_id


    def clean(self):

        content = self.cleaned_data.get("content")
        cause_type = self.cleaned_data.get("cause_type")

        try:
            cause_tag = CauseTag.objects.get(
                content=content, cause_type__id=cause_type.id
            )

        except ObjectDoesNotExist:

            print("原因タグ自体がまだ存在しないか、フォームの入力を間違えている")

            return

        self.cause_tag_cache = cause_tag

        try:
            connect = Connect.objects.get(
                cause_tag=self.cause_tag_cache, answer_id=self.answer_id
            )
            raise forms.ValidationError("その原因タグは既に登録されてます")
        except ObjectDoesNotExist:
            print("その解答にまだその原因タグは登録されていないか、新しく解答を登録しようとしている場合")
            return

    def get_cause_tag_cache(self):

        return self.cause_tag_cache


CauseTagRegisterFormSet = forms.modelformset_factory(
    model=CauseTag, form=CauseTagRegisterForm, extra=1, can_delete=False
)
