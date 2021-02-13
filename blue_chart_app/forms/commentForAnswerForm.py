from django import forms
from blue_chart_app.models.comment_for_answer import CommentForAnswer


class CommentForAnswerForm(forms.ModelForm):
    class Meta:

        model = CommentForAnswer

        fields = {
            "content",
        }

        widgets = {"content": forms.Textarea(attrs={"class": "form-control"})}

        labels = {"content": "コメント"}

        requires = {"content": False}

    def clean_content(self):

        content = self.cleaned_data["content"]
        if len(content) == 0 or content is None:

            raise forms.ValidationError("コメントを入力してください")

        return content
