from django.views import View
from blue_chart_app.forms.evaluationTagForm import EvaluationTagRegisterForm
from django.shortcuts import render, redirect
from blue_chart_app.models.problem import Problem
from blue_chart_app.models.evaluate import Evaluate
from blue_chart_app.models.comment_for_evaluate import CommentForEvaluate
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class EvaluateRegisterView(LoginRequiredMixin, View):
    def get(self, request, problem_id, *args, **kwargs):

        problem = Problem.objects.get(pk=problem_id)

        context = {
            "form": EvaluationTagRegisterForm(request.user.id, problem_id),
            "problem": problem,
        }

        return render(request, "evaluate/register.html", context)

    def post(self, request, problem_id, *args, **kwargs):

        form = EvaluationTagRegisterForm(request.user.id, problem_id, request.POST)
        problem = Problem.objects.get(pk=problem_id)

        if not form.is_valid():

            return render(
                request, "evaluate/register.html", {"form": form, "problem": problem},
            )

        evaluation_tag = form.get_evaluation_tag_cache()

        if evaluation_tag is None:

            evaluation_tag = form.save(commit=True)

        evaluate = Evaluate()
        evaluate.evaluation_tag = evaluation_tag
        evaluate.evaluate_user = request.user
        evaluate.problem = problem
        evaluate.save()

        if form.cleaned_data["comment"] != "":
            comment_for_evaluate = CommentForEvaluate()
            comment_for_evaluate.content = form.cleaned_data["comment"]
            comment_for_evaluate.evaluate = evaluate
            comment_for_evaluate.created_at = timezone.now()
            comment_for_evaluate.updated_at = comment_for_evaluate.created_at
            comment_for_evaluate.comment_user = request.user
            comment_for_evaluate.save()

        messages.success(request, "評価タグを登録しました")

        return redirect("blue_chart_app:problem_show", problem_id=problem.id)


evaluate_register_view = EvaluateRegisterView.as_view()


class EvaluateDeleteView(LoginRequiredMixin, View):
    def post(self, request, evaluate_id, *args, **kwargs):

        evaluate = Evaluate.objects.get(pk=evaluate_id)
        problem_id = evaluate.problem.id
        evaluate.delete()

        messages.success(request, "評価タグを削除しました")

        return redirect("blue_chart_app:problem_show", problem_id=problem_id)


evaluate_delte_view = EvaluateDeleteView.as_view()
