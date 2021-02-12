from django.views import View
from blue_chart_app.models.problem_group import Problem_group
from blue_chart_app.models.problem import Problem
from blue_chart_app.models.subject import Subject
from blue_chart_app.models.latest_connect import LatestConnect
from blue_chart_app.models.evaluate import Evaluate
from blue_chart_app.models.section import Section
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from blue_chart_app.forms.problemForm import SearchForm



class ProblemListView(LoginRequiredMixin, View):
    def get(self, request, problem_group_id, *args, **kwargs):

        problems = Problem.objects.filter(problem_group__id=problem_group_id)
        problem_group = Problem_group.objects.get(pk=problem_group_id)

        return render(
            request,
            "problem/list.html",
            {"problems": problems, "problem_group": problem_group},
        )


problem_list_view = ProblemListView.as_view()


class ProblemSearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        context = {"form": SearchForm()}

        return render(request, "problem/search.html", context)

    def post(self, request, *args, **kwargs):

        form = SearchForm(request.POST)

        if not form.is_valid():
            return render(request, "problem/search.html", {"form": form})

        subject_id = form.cleaned_data["subject"]
        from_page = form.cleaned_data["from_page"]
        to_page = form.cleaned_data["to_page"]
        from_problem_number = form.cleaned_data["from_problem_number"]
        to_problem_number = form.cleaned_data["to_problem_number"]
        exercise_flag = form.cleaned_data["exercise_flag"]
        difficulty = form.cleaned_data["difficulty"]

        queryset = Problem.objects.all()

        subject = None

        if subject_id != "0":

            queryset = queryset.filter(
                problem_group__section__chapter__subject__id=subject_id
            )
            subject = Subject.objects.get(pk=subject_id)

        if from_page is not None and to_page is not None:

            true_from_page = min(from_page, to_page)

            true_to_page = max(from_page, to_page)

            queryset = queryset.filter(page__gte=true_from_page).filter(
                page__lte=true_to_page
            )

        elif from_page is not None:

            queryset = queryset.filter(page__gte=from_page)

        elif to_page is not None:

            queryset = queryset.filter(page__lte=to_page)

        if exercise_flag:

            queryset = queryset.filter(problem_group__name="EXERCISE")

        else:

            if from_problem_number is not None and to_problem_number is not None:

                true_from_problem_number = min(from_problem_number, to_problem_number)

                true_to_problem_number = max(from_problem_number, to_problem_number)

                queryset = queryset.filter(
                    problem_group__number__gte=true_from_problem_number
                ).filter(problem_group__number__lte=true_to_problem_number)

            elif from_problem_number is not None:

                queryset = queryset.filter(
                    problem_group__number__gte=from_problem_number
                )

            elif to_problem_number is not None:

                queryset = queryset.filter(problem_group__number__lte=to_problem_number)

        if difficulty != "0":

            queryset = queryset.filter(difficulty=difficulty)

        problems = queryset

        return render(
            request,
            "problem/result.html",
            {
                "problems": problems,
                "subject": subject,
                "from_page": from_page,
                "to_page": to_page,
                "from_problem_number": from_problem_number,
                "to_problem_number": to_problem_number,
                "exercise_flag": exercise_flag,
                "difficulty": difficulty,
            },
        )


problem_search_view = ProblemSearchView.as_view()


class ProblemShowView(LoginRequiredMixin, View):
    def get(self, request, problem_id, *args, **kwargs):

        problem = Problem.objects.get(pk=problem_id)

        evaluates = Evaluate.objects.select_related("problem").filter(problem=problem)

        return render(
            request, "problem/show.html", {"problem": problem, "evaluates": evaluates}
        )


problem_show_view = ProblemShowView.as_view()


class ProblemListWithCauseTag(LoginRequiredMixin, View):
    def get(self, request, cause_tag_id, section_id, *args, **kwargs):
        
        section = None

        query_set = (
            LatestConnect.objects.select_related("problem", "solve_user", "cause_tag")
            .filter(solve_user__id=request.user.reference_user.id)
            .filter(cause_tag__id=cause_tag_id)
        )

        if section_id == 0:
            latest_connects_with_cause_tag = query_set
        else:
            latest_connects_with_cause_tag = query_set.filter(problem__problem_group__section__id=section_id)
            section = Section.objects.get(pk=section_id)

        return render(
            request,
            "problem/list_with_cause_tag.html",
            {"latest_connects_with_cause_tag": latest_connects_with_cause_tag,
            "section": section},
        )


problem_list_with_cause_tag_view = ProblemListWithCauseTag.as_view()
