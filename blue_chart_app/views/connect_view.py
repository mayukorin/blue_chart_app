from django.views import View
from blue_chart_app.forms.causeTagForm import CauseTagRegisterForm
from django.shortcuts import render, redirect
from blue_chart_app.models.answer import Answer
from blue_chart_app.models.connect import Connect
from blue_chart_app.models.latest_connect import LatestConnect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from blue_chart_app.models.comment_for_connect import CommentForConnect


class ConnectIsOvercomeChangeView(LoginRequiredMixin, View):
    def get(self, request, connect_id, *args, **kwargs):

        connect = Connect.objects.get(pk=connect_id)
        connect.is_overcome = not (connect.is_overcome)
        connect.save()

        return redirect("blue_chart_app:answer_show", answer_id=connect.answer.id)


connect_is_overcome_change_view = ConnectIsOvercomeChangeView.as_view()


class ConnectDeleteView(LoginRequiredMixin, View):
    def post(self, request, connect_id, *args, **kwargs):

        connect = Connect.objects.get(pk=connect_id)
        answer_id = connect.answer.id
        latest_connect = connect.latest_connect

        connect.delete()
        try:
            next_latest_connect = (
                Connect.objects.select_related("latest_connect", "answer")
                .filter(latest_connect__id=latest_connect.id)
                .latest("answer__solve_date")
            )
            latest_connect.connect_model = next_latest_connect
            latest_connect.save()
        except ObjectDoesNotExist:
            latest_connect.delete()

        messages.success(request, "原因タグを取り消しました")
        return redirect("blue_chart_app:answer_show", answer_id=answer_id)


connect_delete_view = ConnectDeleteView.as_view()


class ConnectRegisterView(LoginRequiredMixin, View):
    def get(self, request, answer_id, *args, **kwargs):
        answer = Answer.objects.get(pk=answer_id)

        context = {
            "form": CauseTagRegisterForm(answer_id=answer_id),
            "answer": answer,
        }

        return render(request, "connect/register.html", context)

    def post(self, request, answer_id, *args, **kwargs):
        answer = Answer.objects.get(pk=answer_id)

        form = CauseTagRegisterForm(answer_id, request.POST)
        if not form.is_valid():
            context = {
                "form": form,
                "answer": answer,
            }

            return render(request, "connect/register.html", context)

        if form.cleaned_data["content"] != "" and form.cleaned_data["content"] is not None:

            cause_tag = form.get_cause_tag_cache()

            if cause_tag is None:

                cause_tag = form.save(commit=True)

            try:
                latest_connect_for_cause_tag = LatestConnect.objects.get(
                    problem__id=answer.problem.id,
                    solve_user__id=request.user.reference_user.id,
                    cause_tag__id=cause_tag.id,
                )

            except ObjectDoesNotExist:

                latest_connect_for_cause_tag = LatestConnect()
                latest_connect_for_cause_tag.problem = answer.problem
                latest_connect_for_cause_tag.solve_user = request.user.reference_user
                latest_connect_for_cause_tag.cause_tag = cause_tag
                latest_connect_for_cause_tag.save()

            connect = Connect()
            connect.answer = answer
            connect.connect_user = request.user
            connect.cause_tag = cause_tag
            connect.latest_connect = latest_connect_for_cause_tag
            connect.is_overcome = False
            connect.save()
            if (
                latest_connect_for_cause_tag.connect_model is None
                or latest_connect_for_cause_tag.connect_model.answer.solve_date
                < answer.solve_date
            ):
                latest_connect_for_cause_tag.connect_model = connect
                latest_connect_for_cause_tag.save()

            if form.cleaned_data["comment_for_connect"] != "":

                comment_for_connect = CommentForConnect()
                comment_for_connect.comment_user = request.user
                comment_for_connect.content = form.cleaned_data["comment_for_connect"]
                created_at = timezone.now()
                comment_for_connect.created_at = created_at
                comment_for_connect.updated_at = created_at
                comment_for_connect.connect = connect
                comment_for_connect.save()

            messages.success(request, "新しい原因タグを登録しました")
        return redirect("blue_chart_app:answer_show", answer_id=answer_id)


connect_register_view = ConnectRegisterView.as_view()
