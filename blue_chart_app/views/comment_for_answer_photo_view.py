# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 12:39:35 2021

@author: Mayuko
"""
from django.views import View
from blue_chart_app.forms.commentForAnswerPhotoForm import CommentForAnswerPhotoForm
from django.shortcuts import render, redirect
from blue_chart_app.models.answer_photo import AnswerPhoto
from blue_chart_app.models.comment_for_answer_photo import CommentForAnswerPhoto
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class CommentForAnswerPhotoRegisterView(LoginRequiredMixin, View):
    def get(self, request, answer_photo_id, *args, **kwargs):

        answer_photo = AnswerPhoto.objects.get(pk=answer_photo_id)
        form = CommentForAnswerPhotoForm()

        return render(
            request,
            "comment_for_answer_photo/register.html",
            {"form": form, "answer_photo": answer_photo},
        )

    def post(self, request, answer_photo_id, *args, **kwargs):

        form = CommentForAnswerPhotoForm(request.POST)
        answer_photo = AnswerPhoto.objects.get(pk=answer_photo_id)

        if not form.is_valid():

            return render(
                request,
                "comment_for_answer_photo/register.html",
                {"form": form, "answer_photo": answer_photo},
            )

        comment_for_answer_photo = form.save(commit=False)
        created_at = timezone.now()
        comment_for_answer_photo.created_at = created_at
        comment_for_answer_photo.updated_at = created_at
        comment_for_answer_photo.comment_user = request.user
        comment_for_answer_photo.answer_photo = answer_photo

        comment_for_answer_photo.save()
        messages.success(request, "コメントを追加しました")
        return redirect("blue_chart_app:answer_show", answer_id=answer_photo.answer.id)


comment_for_answer_photo_register_view = CommentForAnswerPhotoRegisterView.as_view()


class CommentForAnswerPhotoUpdateView(LoginRequiredMixin, View):
    def get(self, request, comment_for_answer_photo_id, *args, **kwargs):

        comment_for_answer_photo = CommentForAnswerPhoto.objects.get(
            pk=comment_for_answer_photo_id
        )
        form = CommentForAnswerPhotoForm(instance=comment_for_answer_photo)

        return render(
            request,
            "comment_for_answer_photo/update.html",
            {"form": form, "comment_for_answer_photo": comment_for_answer_photo},
        )

    def post(self, request, comment_for_answer_photo_id, *args, **kwargs):

        comment_for_answer_photo = CommentForAnswerPhoto.objects.get(
            pk=comment_for_answer_photo_id
        )
        form = CommentForAnswerPhotoForm(
            request.POST, instance=comment_for_answer_photo
        )

        if not form.is_valid():

            return render(
                request,
                "comment_for_answer_photo/update.html",
                {"form": form, "comment_for_answer_photo": comment_for_answer_photo},
            )

        comment_for_answer_photo = form.save(commit=False)
        comment_for_answer_photo.updated_at = timezone.now()

        comment_for_answer_photo.save()
        messages.success(request, "コメントの編集が完了しました")
        return redirect(
            "blue_chart_app:answer_show",
            answer_id=comment_for_answer_photo.answer_photo.answer.id,
        )


comment_for_answer_photo_update_view = CommentForAnswerPhotoUpdateView.as_view()


class CommentForAnswerPhotoDeleteView(LoginRequiredMixin, View):
    def post(self, request, comment_for_answer_photo_id, *args, **kwargs):

        comment_for_answer_photo = CommentForAnswerPhoto.objects.get(
            pk=comment_for_answer_photo_id
        )
        answer_id = comment_for_answer_photo.answer_photo.answer.id

        comment_for_answer_photo.delete()
        messages.success(request, "コメントを削除しました")

        return redirect("blue_chart_app:answer_show", answer_id=answer_id)


comment_for_answer_photo_delete_view = CommentForAnswerPhotoDeleteView.as_view()
