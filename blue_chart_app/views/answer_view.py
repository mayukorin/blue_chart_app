# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 21:35:55 2021

@author: Mayuko
"""


from django.views import View
from blue_chart_app.forms.answerForm import AnswerRegisterForm, AnswerUpdateForm
from blue_chart_app.forms.causeTagForm import CauseTagRegisterFormSet
from django.shortcuts import render, redirect
from blue_chart_app.models.problem import Problem
from blue_chart_app.models.answer_photo import AnswerPhoto
from blue_chart_app.models.comment_for_answer_photo import CommentForAnswerPhoto
from blue_chart_app.models.answer import Answer
from blue_chart_app.models.cause_tag import CauseTag
from blue_chart_app.models.section import Section
from blue_chart_app.models.comment_for_connect import CommentForConnect
from blue_chart_app.models.latest_connect import LatestConnect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from blue_chart_app.models.connect import Connect
from blue_chart_app.forms.connectForm import ConnectForNotOvercomeLatestConnectsForm
import os
from cloudinary import CloudinaryImage
import cloudinary, cloudinary.uploader, cloudinary.forms, cloudinary.api


class AnswerRegisterView(LoginRequiredMixin, View):
    def get(self, request, problem_id, *args, **kwargs):

        problem = Problem.objects.get(pk=problem_id)

        form = AnswerRegisterForm()
        new_cause_tags_formset = CauseTagRegisterFormSet(
            queryset=CauseTag.objects.none()
        )

        not_overcome_latest_connects = (
            LatestConnect.objects.filter(solve_user__id=request.user.reference_user.id)
            .filter(connect_model__is_overcome=False)
            .filter(problem__id=problem_id)
            .order_by("-id")
        )
        new_connects_forms = [
            ConnectForNotOvercomeLatestConnectsForm(
                latest_connect=not_overcome_latest_connect,
                prefix=not_overcome_latest_connect.id,
            )
            for not_overcome_latest_connect in not_overcome_latest_connects
        ]

        return render(
            request,
            "answer/register.html",
            {
                "form": form,
                "formset": new_cause_tags_formset,
                "new_connects_forms": new_connects_forms,
                "problem": problem,
            },
        )

    def post(self, request, problem_id, *args, **kwargs):

        form = AnswerRegisterForm(request.POST, request.FILES)
        new_cause_tags_formset = CauseTagRegisterFormSet(request.POST)
        problem = Problem.objects.get(pk=problem_id)

        not_overcome_latest_connects = (
            LatestConnect.objects.filter(solve_user__id=request.user.reference_user.id)
            .filter(connect_model__is_overcome=False)
            .filter(problem__id=problem_id)
            .order_by("-id")
        )
        new_connects_forms = [
            ConnectForNotOvercomeLatestConnectsForm(
                not_overcome_latest_connect,
                request.POST,
                prefix=not_overcome_latest_connect.id,
            )
            for not_overcome_latest_connect in not_overcome_latest_connects
        ]

        if not form.is_valid() or not new_cause_tags_formset.is_valid():

            return render(
                request,
                "answer/register.html",
                {
                    "form": form,
                    "formset": new_cause_tags_formset,
                    "new_connects_forms": new_connects_forms,
                    "problem": problem,
                },
            )

        problem = Problem.objects.get(pk=problem_id)

        answer = form.save(commit=False)
        answer.problem = problem
        answer.student = request.user.reference_user
        answer.save()

        answer_photo = None

        if form.cleaned_data["answer_photo"] is not None:

            answer_photo = AnswerPhoto()

            answer_photo.image = form.cleaned_data["answer_photo"]
            answer_photo.answer = answer
            answer_photo.upload_user = request.user
            answer_photo.save()

            if form.cleaned_data["comment_for_answer_photo"] != "":

                comment_for_answer_photo = CommentForAnswerPhoto()
                comment_for_answer_photo.content = form.cleaned_data[
                    "comment_for_answer_photo"
                ]
                comment_for_answer_photo.comment_user = request.user
                current_time = timezone.now()
                comment_for_answer_photo.created_at = current_time
                comment_for_answer_photo.updated_at = current_time
                comment_for_answer_photo.answer_photo = answer_photo

                comment_for_answer_photo.save()

        if form.cleaned_data.get("solve_date") is not None:

            for new_connect_form in new_connects_forms:
                if not new_connect_form.is_valid():

                    return render(
                        request,
                        "answer/register.html",
                        {
                            "form": form,
                            "formset": new_cause_tags_formset,
                            "new_connects_forms": new_connects_forms,
                            "problem": problem,
                        },
                    )

            for new_connect_form in new_connects_forms:

                connect = Connect()
                connect.connect_user = request.user
                connect.cause_tag = new_connect_form.get_cause_tag_cache()
                connect.latest_connect = new_connect_form.get_latest_connect_cache()
                connect.answer = answer
                connect.is_overcome = new_connect_form.cleaned_data["is_overcome"]
                connect.save()

                latest_connect = new_connect_form.get_latest_connect_cache()
                if latest_connect.connect_model.answer.solve_date < form.cleaned_data.get(
                    "solve_date"
                ):
                    latest_connect.connect_model = connect
                    latest_connect.save()

            for form in new_cause_tags_formset:

                if form.cleaned_data["content"] is not None:

                    cause_tag = form.get_cause_tag_cache()

                    if cause_tag is None:

                        cause_tag = form.save(commit=True)

                    try:
                        latest_connect_for_cause_tag = LatestConnect.objects.get(
                            problem__id=problem_id,
                            solve_user__id=request.user.reference_user.id,
                            cause_tag__id=cause_tag.id,
                        )

                    except ObjectDoesNotExist:

                        latest_connect_for_cause_tag = LatestConnect()
                        latest_connect_for_cause_tag.problem = problem
                        latest_connect_for_cause_tag.solve_user = (
                            request.user.reference_user
                        )
                        latest_connect_for_cause_tag.cause_tag = cause_tag
                        latest_connect_for_cause_tag.save()

                    if (
                        latest_connect_for_cause_tag.connect_model is None
                        or latest_connect_for_cause_tag.cause_tag.id
                        not in [
                            not_overcome_latest_connect.cause_tag.id
                            for not_overcome_latest_connect in not_overcome_latest_connects
                        ]
                    ):

                        connect = Connect()
                        connect.answer = answer
                        connect.connect_user = request.user
                        connect.is_overcome = False
                        connect.cause_tag = cause_tag
                        connect.latest_connect = latest_connect_for_cause_tag
                        connect.save()

                        if form.cleaned_data["comment_for_connect"] != "":
                            comment_for_connect = CommentForConnect()
                            comment_for_connect.comment_user = request.user
                            comment_for_connect.content = form.cleaned_data[
                                "comment_for_connect"
                            ]
                            current_time = timezone.now()
                            comment_for_connect.created_at = current_time
                            comment_for_connect.updated_at = current_time
                            comment_for_connect.connect = connect
                            comment_for_connect.save()

                        if (
                            latest_connect_for_cause_tag.connect_model is None
                            or latest_connect_for_cause_tag.connect_model.answer.solve_date
                            < answer.solve_date
                        ):

                            latest_connect_for_cause_tag.connect_model = connect
                            latest_connect_for_cause_tag.save()

        messages.success(request, "勉強記録を新規登録しました")

        return redirect(
            "blue_chart_app:answer_list_with_problem", problem_id=problem_id
        )


answer_register_view = AnswerRegisterView.as_view()


class AnswerUpdateView(LoginRequiredMixin, View):
    def get(self, request, answer_id, *args, **kwargs):

        answer = Answer.objects.get(pk=answer_id)
        form = AnswerUpdateForm(instance=answer)

        return render(request, "answer/update.html", {"form": form, "answer": answer})

    def post(self, request, answer_id, *args, **kwargs):

        answer = Answer.objects.get(pk=answer_id)
        form = AnswerUpdateForm(request.POST, instance=answer)

        if not form.is_valid():

            return render(
                request, "answer/update.html", {"form": form, "answer": answer}
            )

        answer = form.save(commit=True)

        messages.success(request, "勉強記録を更新しました")
        return redirect("blue_chart_app:answer_show", answer_id=answer.id)


answer_update_view = AnswerUpdateView.as_view()


class AnswerListWithProblemView(LoginRequiredMixin, View):
    def get(self, request, problem_id, *args, **kwargs):

        problem = Problem.objects.get(pk=problem_id)
        answers = (
            Answer.objects.filter(problem__id=problem_id)
            .filter(student=request.user.reference_user)
            .order_by("-solve_plan_date")
        )

        return render(
            request,
            "answer/list_with_problem.html",
            {"answers": answers, "problem": problem},
        )


answer_list_with_problem_view = AnswerListWithProblemView.as_view()


class AnswerAllListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        answers = Answer.objects.filter(student=request.user.reference_user).order_by(
            "-solve_plan_date"
        )

        return render(request, "answer/all_list.html", {"answers": answers})


answer_all_list_view = AnswerAllListView.as_view()


class AnswerShowView(LoginRequiredMixin, View):
    def get(self, request, answer_id, *args, **kwargs):

        answer = Answer.objects.get(pk=answer_id)

        return render(request, "answer/show.html", {"answer": answer})


answer_show_view = AnswerShowView.as_view()


class AnswerListWithCauseTagView(LoginRequiredMixin, View):
    def get(self, request, problem_id, cause_tag_id, section_id, *args, **kwargs):

        answer_list = (
            Answer.objects.select_related("problem")
            .filter(student__id=request.user.reference_user.id)
            .filter(problem__id=problem_id)
            .order_by("-solve_date")
        )
        cause_tag = CauseTag.objects.get(pk=cause_tag_id)
        section = None
        if section_id != 0:
            section = Section.objects.get(pk=section_id)
        return render(
            request,
            "answer/list_with_cause_tag.html",
            {"answer_list": answer_list, "cause_tag": cause_tag, "section": section},
        )


answer_list_with_cause_tag_view = AnswerListWithCauseTagView.as_view()


class AnswerDeleteView(LoginRequiredMixin, View):
    def post(self, request, answer_id, *args, **kwargs):

        answer = Answer.objects.get(pk=answer_id)
        problem_id = answer.problem.id

        answer_photos = AnswerPhoto.objects.select_related("answer").filter(
            answer__id=answer_id
        )
        for answer_photo in answer_photos[:]:
            comments_for_answer_photo = CommentForAnswerPhoto.objects.filter(
                answer_photo__id=answer_photo.id
            ).delete()
            if str(answer_photo.image) != "":
                # ret = cloudinary.uploader.destroy(public_id = str(answer_photo.image))
                os.remove(str(answer_photo.image))

        connects = Connect.objects.select_related("answer").filter(answer__id=answer_id)
        for connect in connects:

            if connect.latest_connect.connect_model.id == connect.id:

                latest_connect = connect.latest_connect
                try:
                    next_latest_connect = (
                        Connect.objects.select_related("latest_connect", "answer")
                        .filter(latest_connect__id=latest_connect.id)
                        .exclude(answer__id=answer_id)
                        .latest("answer__solve_date")
                    )
                    latest_connect.connect_model = next_latest_connect
                    latest_connect.save()
                except ObjectDoesNotExist:

                    latest_connect.delete()

        answer.delete()

        messages.success(request, "解答情報を削除しました")

        return redirect(
            "blue_chart_app:answer_list_with_problem", problem_id=problem_id
        )


answer_delete_view = AnswerDeleteView.as_view()
