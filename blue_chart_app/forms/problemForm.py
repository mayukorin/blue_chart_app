# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 12:17:24 2020

@author: Mayuko
"""


from django import forms


class SearchForm(forms.Form):

    subject = forms.fields.ChoiceField(
        choices=(("0", "-"), ("1", "数学Ⅰ"), ("2", "数学A"), ("3", "数学Ⅱ"), ("4", "数学B")),
        label="教科",
    )

    from_page = forms.IntegerField(
        widget=forms.NumberInput(attrs={"min": "1"}), required=False
    )

    to_page = forms.IntegerField(
        widget=forms.NumberInput(attrs={"min": "1"}), required=False
    )

    from_problem_number = forms.IntegerField(
        widget=forms.NumberInput(attrs={"min": "1"}), required=False
    )

    to_problem_number = forms.IntegerField(
        widget=forms.NumberInput(attrs={"min": "1"}), required=False
    )

    exercise_flag = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="EXERCISEを検索する",
    )

    difficulty = forms.fields.ChoiceField(
        choices=(
            ("0", "-"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
        ),
        label="難易度",
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.label != "EXERCISEを検索する":
                field.widget.attrs.update({"class": "form-control"})
