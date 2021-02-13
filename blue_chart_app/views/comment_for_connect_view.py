from django.views import View
from django.shortcuts import render, redirect
from blue_chart_app.models.connect import Connect
from blue_chart_app.models.comment_for_connect import CommentForConnect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from blue_chart_app.forms.commentForConnectForm import CommentForConnectForm


class CommentForConnectRegisterView(LoginRequiredMixin, View):
    def get(self, request, connect_id, *args, **kwargs):

        connect = Connect.objects.get(pk=connect_id)
        context = {
            "connect": connect,
            "form": CommentForConnectForm(),
        }
        return render(request, "comment_for_connect/register.html", context)

    def post(self, request, connect_id, *args, **kwargs):

        form = CommentForConnectForm(request.POST)
        connect = Connect.objects.get(pk=connect_id)

        context = {
            "connect": connect,
            "form": form,
        }
        if not form.is_valid():
            return render(request, "comment_for_connect/register.html", context)

        comment_for_connect = form.save(commit=False)
        comment_for_connect.comment_user = request.user
        current_time = timezone.now()
        comment_for_connect.created_at = current_time
        comment_for_connect.updated_at = current_time
        comment_for_connect.connect = connect
        comment_for_connect.save()

        messages.success(request, "原因タグについてのコメントをしました")
        return redirect("blue_chart_app:answer_show", answer_id=connect.answer.id)


comment_for_connect_register_view = CommentForConnectRegisterView.as_view()


class CommentForConnectUpdateView(LoginRequiredMixin, View):
    def get(self, request, comment_for_connect_id, *args, **kwargs):

        comment_for_connect = CommentForConnect.objects.get(pk=comment_for_connect_id)

        form = CommentForConnectForm(instance=comment_for_connect)

        return render(
            request,
            "comment_for_connect/update.html",
            {"form": form, "comment_for_connect": comment_for_connect},
        )

    def post(self, request, comment_for_connect_id, *args, **kwargs):

        comment_for_connect = CommentForConnect.objects.get(pk=comment_for_connect_id)

        form = CommentForConnectForm(request.POST, instance=comment_for_connect)

        if not form.is_valid():
            return render(
                request,
                "comment_for_connect/update.html",
                {"form": form, "comment_for_connect": comment_for_connect},
            )

        form.save(commit=True)

        messages.success(request, "原因タグについてのコメントを編集しました")
        return redirect(
            "blue_chart_app:answer_show",
            answer_id=comment_for_connect.connect.answer.id,
        )


comment_for_connect_update_view = CommentForConnectUpdateView.as_view()


class CommentForConnectDelteView(LoginRequiredMixin, View):
    def post(self, request, comemnt_for_connect_id, *args, **kwargs):

        comemnt_for_connect = CommentForConnect.objects.get(pk=comemnt_for_connect_id)
        answer_id = comemnt_for_connect.connect.answer.id
        comemnt_for_connect.delete()

        messages.success(request, "原因タグについてのコメントを削除しました")
        return redirect("blue_chart_app:answer_show", answer_id=answer_id)


comment_for_connect_delete_view = CommentForConnectDelteView.as_view()
