# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 18:08:25 2021

@author: Mayuko
"""
from django.views import View
from django.shortcuts import render, redirect
from blue_chart_app.models.answer_photo import AnswerPhoto
from blue_chart_app.models.comment_for_answer_photo import CommentForAnswerPhoto
from blue_chart_app.models.answer import Answer
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from blue_chart_app.forms.answerPhotoForm import AnswerPhotoRegisterForm
import os
from cloudinary import CloudinaryImage
import cloudinary, cloudinary.uploader, cloudinary.forms, cloudinary.api


class AnswerPhotoRegisterView(LoginRequiredMixin, View):
    def get(self, request, answer_id, *args, **kwargs):

        answer = Answer.objects.get(pk=answer_id)
        form = AnswerPhotoRegisterForm()

        return render(
            request, "answer_photo/register.html", {"form": form, "answer": answer}
        )

    def post(self, request, answer_id, *args, **kwargs):

        answer = Answer.objects.get(pk=answer_id)
        form = AnswerPhotoRegisterForm(request.POST, request.FILES)

        if not form.is_valid():

            return render(
                request, "ansewr_photo/register.html", {"form": form, "answer": answer}
            )

        answer_photo = form.save(commit=False)
        answer_photo.answer = answer
        answer_photo.upload_user = request.user
        answer_photo.uploaded_at = timezone.now()

        answer_photo.save()

        if form.cleaned_data["comment"] != "":
            comment_for_answer_photo = CommentForAnswerPhoto()
            comment_for_answer_photo.content = form.cleaned_data["comment"]
            comment_for_answer_photo.comment_user = request.user
            comment_for_answer_photo.answer_photo = answer_photo
            current_time = timezone.now()
            comment_for_answer_photo.created_at = current_time
            comment_for_answer_photo.updated_at = current_time

            comment_for_answer_photo.save()

        messages.success(request, "解答写真の登録が完了しました")
        return redirect("blue_chart_app:answer_show", answer_id=answer_id)


answer_photo_register_view = AnswerPhotoRegisterView.as_view()


class AnswerPhotoDeleteView(LoginRequiredMixin, View):
    def post(self, request, answer_photo_id, *args, **kwargs):

        answer_photo = AnswerPhoto.objects.get(pk=answer_photo_id)
        #ret = cloudinary.uploader.destroy(public_id = str(answer_photo.image))
        os.remove(str(answer_photo.image))

        answer_photo.image = ""
        answer_photo.save()

        messages.success(request, "解答写真を削除しました")

        return redirect("blue_chart_app:answer_show", answer_id=answer_photo.answer.id)


answer_photo_delete_view = AnswerPhotoDeleteView.as_view()
