from blue_chart_app.models.comment_for_evaluate import CommentForEvaluate
from django import forms


class CommentForEvaluateForm(forms.ModelForm):
    class Meta:
        model = CommentForEvaluate

        fields = {
            "content",
        }

        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }

        labels = {
            "content": "コメント",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False

    def clean_content(self):

        content = self.cleaned_data["content"]

        if len(content) == 0:
            raise forms.ValidationError("コメントを入力してください")

        return content
