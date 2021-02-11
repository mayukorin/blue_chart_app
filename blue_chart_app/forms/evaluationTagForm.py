# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 16:22:52 2021

@author: Mayuko
"""


from django import forms
from blue_chart_app.models.evaluation_tag import EvaluationTag
from blue_chart_app.models.type import Type
from blue_chart_app.models.evaluate import Evaluate
from django.core.exceptions import ObjectDoesNotExist
from blue_chart_app.widgets import SuggestWidget
from django.urls import reverse_lazy


class EvaluationTagRegisterForm(forms.ModelForm):
    class Meta:
        model = EvaluationTag

        fields = (
            "evaluation_type",
            "content",
        )

        labels = {"content": "評価タグの内容", "evaluation_type": "主に身につく力"}

        widgets = {
            "content": SuggestWidget(
                attrs={
                    "data-url": reverse_lazy("blue_chart_app:evaluation_tag_suggest"),
                    "name": "content",
                }
            ),
            "evaluation_type": forms.Select(attrs={"class": "form-control"}),
        }

    evaluation_type = forms.ModelChoiceField(
        queryset=Type.objects.all().order_by("id"),
        empty_label=None,
        label="主に身につくこと",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    comment = forms.CharField(
        label="コメント（任意）",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )

    def __init__(self, user_id, problem_id, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.user_id = user_id
        self.problem_id = problem_id
        self.evaluation_tag_cache = None
        self.fields["content"].required = False

        if self.errors and "content" in self.errors:

            self.fields["content"].widget.attrs.update(
                {"class": "form-control is-invalid suggest"}
            )

    def clean_content(self):

        content = self.cleaned_data["content"]
        if content is None:

            raise forms.ValidationError("評価タグの内容を入力してください")

        return content

    def clean(self):

        content = self.cleaned_data.get("content")
        evaluation_type = self.cleaned_data.get("evaluation_type")

        try:
            evaluation_tag = EvaluationTag.objects.get(
                content=content, evaluation_type__id=evaluation_type.id
            )

        except ObjectDoesNotExist:

            print("評価タグ自体がまだ存在しないか、フォームの入力を間違えている")

            return

        self.evaluation_tag_cache = evaluation_tag

        try:
            evaluate = Evaluate.objects.get(
                evaluation_tag__id=self.evaluation_tag_cache.id,
                problem__id=self.problem_id,
            )

        except ObjectDoesNotExist:

            print("まだその評価タグはその問題に登録されていない")

            return

        raise forms.ValidationError("その問題に対するその評価タグは既に登録されています")

    def get_evaluation_tag_cache(self):

        return self.evaluation_tag_cache


class EvaluationTagSearchForm(forms.Form):

    content_keyword = forms.CharField(
        label="評価タグ名",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
