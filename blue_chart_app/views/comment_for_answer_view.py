from django.views import View
from blue_chart_app.forms.commentForAnswerForm import CommentForAnswerForm
from django.shortcuts import render, redirect
from blue_chart_app.models.comment_for_answer import CommentForAnswer
from blue_chart_app.models.answer import Answer
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class CommentForAnswerRegisterView(LoginRequiredMixin, View):
    def get(self, request, answer_id, *args, **kwargs):

        context = {
            "answer": Answer.objects.get(pk=answer_id),
            "form": CommentForAnswerForm(),
        }

        return render(request, "comment_for_answer/register.html", context)

    def post(self, request, answer_id, *args, **kwargs):

        answer = Answer.objects.get(pk=answer_id)
        form = CommentForAnswerForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                "comment_for_answer/register.html",
                {"answer": answer, "form": form},
            )

        comment_for_answer = form.save(commit=False)
        comment_for_answer.comment_user = request.user
        comment_for_answer.answer = answer
        current_time = timezone.now()
        comment_for_answer.created_at = current_time
        comment_for_answer.updated_at = current_time

        comment_for_answer.save()
        messages.success(request, "解答に対するコメントを登録しました")

        return redirect("blue_chart_app:answer_show", answer_id=answer.id)


comment_for_answer_register_view = CommentForAnswerRegisterView.as_view()


class CommentForAnswerUpdateView(LoginRequiredMixin, View):
    def get(self, request, comment_for_answer_id, *args, **kwargs):

        comment_for_answer = CommentForAnswer.objects.get(pk=comment_for_answer_id)
        context = {
            "comment_for_answer": comment_for_answer,
            "form": CommentForAnswerForm(instance=comment_for_answer),
        }

        return render(request, "comment_for_answer/update.html", context)

    def post(self, request, comment_for_answer_id, *args, **kwargs):

        comment_for_answer = CommentForAnswer.objects.get(pk=comment_for_answer_id)
        form = CommentForAnswerForm(request.POST, instance=comment_for_answer)

        if not form.is_valid():
            return render(
                request,
                "comment_for_answer/update.html",
                {"comment_for_answer": comment_for_answer, "form": form},
            )

        comment_for_answer = form.save(commit=False)
        comment_for_answer.updated_at = timezone.now()

        comment_for_answer.save()
        messages.success(request, "解答に対するコメントを編集しました")

        return redirect(
            "blue_chart_app:answer_show", answer_id=comment_for_answer.answer.id
        )


comment_for_answer_update_view = CommentForAnswerUpdateView.as_view()


class CommentForAnswerDeleteView(LoginRequiredMixin, View):
    def post(self, request, comment_for_answer_id, *args, **kwargs):

        comment_for_answer = CommentForAnswer.objects.get(pk=comment_for_answer_id)
        answer_id = comment_for_answer.answer.id

        comment_for_answer.delete()

        messages.success(request, "コメントを削除しました")

        return redirect("blue_chart_app:answer_show", answer_id=answer_id)


comment_for_answer_delete_view = CommentForAnswerDeleteView.as_view()
