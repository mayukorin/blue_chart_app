from django import forms
from blue_chart_app.models.comment_for_connect import CommentForConnect


class CommentForConnectForm(forms.ModelForm):
    class Meta:

        model = CommentForConnect

        fields = {"content"}

        widgets = {"content": forms.Textarea(attrs={"class": "form-control"})}

        labels = {"content": "コメント"}

        requires = {"content": False}

    def clean_content(self):

        content = self.cleaned_data["content"]

        if len(content) == 0 or content is None:

            raise forms.ValidationError("コメントを入力してください")

        return content
