from django.views import View
from django.shortcuts import render
from blue_chart_app.models.chapter import Chapter
from blue_chart_app.models.connect import Connect
from blue_chart_app.models.latest_connect import LatestConnect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from blue_chart_app.models.section import Section
from django.http import JsonResponse


class CauseTagListView(LoginRequiredMixin, View):
    def get(self, request, section_id, *args, **kwargs):

        queryset = (
            LatestConnect.objects.select_related()
            .filter(solve_user__id=request.user.reference_user.id)
            .filter(connect_model__is_overcome=False)
        )
        overcome_queryset = (
            LatestConnect.objects.select_related()
            .filter(solve_user__id=request.user.reference_user.id)
            .filter(connect_model__is_overcome=True)
        )
        section = None

        if section_id == 0:
            not_overcome_cause_tags = queryset.values(
                "cause_tag__id", "cause_tag__cause_type__id", "cause_tag__content"
            ).annotate(total=Count("cause_tag"))
            overcome_cause_tags = overcome_queryset.values(
                "cause_tag__id", "cause_tag__cause_type__id", "cause_tag__content"
            ).annotate(total=Count("cause_tag"))

        else:
            not_overcome_cause_tags = (
                queryset.filter(problem__problem_group__section__id=section_id)
                .values(
                    "cause_tag__id", "cause_tag__cause_type__id", "cause_tag__content"
                )
                .annotate(total=Count("cause_tag"))
            )
            overcome_cause_tags = (
                overcome_queryset.filter(problem__problem_group__section__id=section_id)
                .values(
                    "cause_tag__id", "cause_tag__cause_type__id", "cause_tag__content"
                )
                .annotate(total=Count("cause_tag"))
            )
            section = Section.objects.get(pk=section_id)

        return render(
            request,
            "cause_tag/list.html",
            {
                "not_overcome_cause_tags": not_overcome_cause_tags,
                "overcome_cause_tags": overcome_cause_tags,
                "section": section,
            },
        )


cause_tag_list_view = CauseTagListView.as_view()


class CauseTagGraph(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        chapters = Chapter.objects.all()

        return render(
            request,
            "cause_tag/graph.html",
            {"chapters": chapters},
        )


cause_tag_graph = CauseTagGraph.as_view()


class ConnectsCountBySectionAndCauseTagType(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        chapter_id = request.GET["chapter_id"]
        sections = Section.objects.filter(chapter__id=chapter_id).values()
        connects_count = {}
        for cause_tag_type_id in range(1, 4):
            
            connects_by_section_and_cause_tag_type = (
                Connect.objects.select_related()
                .filter(answer__student__id=request.user.reference_user.id)
                .filter(latest_connect__connect_model__is_overcome=False)
                .filter(answer__problem__problem_group__section__chapter__id=chapter_id)
                .filter(cause_tag__cause_type__id=cause_tag_type_id)
                .values("answer__problem__problem_group__section__id")
                .annotate(total=Count("answer__problem__problem_group__section__id"))
            )
            section_id_and_connects_by_section_and_cause_tag_type_total = {
                str(c["answer__problem__problem_group__section__id"]): c["total"]
                for c in connects_by_section_and_cause_tag_type
            }
            connects_count_by_cause_tag_type = []

            for section in sections:
                if (
                    section_id_and_connects_by_section_and_cause_tag_type_total.get(
                        str(section["id"])
                    )
                    is None
                ):
                    connects_count_by_cause_tag_type.append(0)
                else:
                    connects_count_by_cause_tag_type.append(
                        section_id_and_connects_by_section_and_cause_tag_type_total.get(
                            str(section["id"])
                        )
                    )

            connects_count[cause_tag_type_id] = connects_count_by_cause_tag_type

        sections_id = [section["id"] for section in sections]
        sections_name = [
            "§" + str(section["number"]) + section["name"] for section in sections
        ]
        return JsonResponse(
            {
                "connects_count": connects_count,
                "sections_name": sections_name,
                "sections_id": sections_id,
            }
        )


connects_count = ConnectsCountBySectionAndCauseTagType.as_view()
