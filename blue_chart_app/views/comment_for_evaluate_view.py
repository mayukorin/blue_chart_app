from django.views import View
from blue_chart_app.models.evaluate import Evaluate
from blue_chart_app.models.comment_for_evaluate import CommentForEvaluate
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from blue_chart_app.forms.commentForEvaluateForm import CommentForEvaluateForm
from django.utils import timezone


class CommentForEvaluateRegisterView(LoginRequiredMixin, View):
    def get(self, request, evaluate_id, *args, **kwargs):

        context = {
            "evaluate": Evaluate.objects.get(pk=evaluate_id),
            "form": CommentForEvaluateForm(),
        }

        return render(request, "comment_for_evaluate/register.html", context)

    def post(self, request, evaluate_id, *args, **kwargs):

        evaluate = Evaluate.objects.get(pk=evaluate_id)
        form = CommentForEvaluateForm(request.POST)

        if not form.is_valid():

            return render(
                request,
                "comment_for_evaluate/register.html",
                {"evaluate": evaluate, "form": form},
            )

        comment_for_evaluate = form.save(commit=False)
        comment_for_evaluate.evaluate = evaluate
        comment_for_evaluate.comment_user = request.user
        comment_for_evaluate.created_at = timezone.now()
        comment_for_evaluate.updated_at = comment_for_evaluate.created_at
        comment_for_evaluate.save()

        messages.success(request, "評価タグへのコメントが完了しました")

        return redirect("blue_chart_app:problem_show", problem_id=evaluate.problem.id)


comment_for_evaluate_register_view = CommentForEvaluateRegisterView.as_view()


class CommentForEvaluateUpdateView(LoginRequiredMixin, View):
    def get(self, request, comment_for_evaluate_id, *args, **kwargs):
        comment_for_evaluate = CommentForEvaluate.objects.get(
            pk=comment_for_evaluate_id
        )
        context = {
            "comment_for_evaluate": comment_for_evaluate,
            "form": CommentForEvaluateForm(instance=comment_for_evaluate),
        }

        return render(request, "comment_for_evaluate/update.html", context)

    def post(self, request, comment_for_evaluate_id, *args, **kwargs):
        comment_for_evaluate = CommentForEvaluate.objects.get(
            pk=comment_for_evaluate_id
        )
        form = CommentForEvaluateForm(request.POST, instance=comment_for_evaluate)

        if not form.is_valid():

            return render(
                request,
                "comment_for_evaluate/update.html",
                {"comment_for_evaluate": comment_for_evaluate, "form": form},
            )

        comment_for_evaluate = form.save(commit=False)
        comment_for_evaluate.updated_at = timezone.now()

        comment_for_evaluate.save()

        messages.success(request, "評価タグへのコメントの更新が完了しました")

        return redirect(
            "blue_chart_app:problem_show",
            problem_id=comment_for_evaluate.evaluate.problem.id,
        )


comment_for_evaluate_update_view = CommentForEvaluateUpdateView.as_view()


class CommentForEvaluateDeleteView(LoginRequiredMixin, View):
    def post(self, request, comment_for_evaluate_id, *args, **kwrags):

        comment_for_evaluate = CommentForEvaluate.objects.get(
            pk=comment_for_evaluate_id
        )
        problem_id = comment_for_evaluate.evaluate.problem.id

        comment_for_evaluate.delete()

        messages.success(request, "評価タグへのコメントの削除が完了しました")
        return redirect("blue_chart_app:problem_show", problem_id=problem_id)


comment_for_evaluate_delete_view = CommentForEvaluateDeleteView.as_view()
