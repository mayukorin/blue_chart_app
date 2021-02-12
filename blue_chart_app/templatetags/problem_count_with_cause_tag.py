from django import template
from blue_chart_app.models.latest_connect import LatestConnect
from django.core.exceptions import ObjectDoesNotExist


register = template.Library()

@register.simple_tag
def problem_count_with_cause_tag(reference_user_id, cause_tag_id, section_id, is_overcome):

    queryset = (
            LatestConnect.objects.select_related()
            .filter(solve_user__id=reference_user_id)
            .filter(cause_tag__id=cause_tag_id)
            .filter(connect_model__is_overcome=is_overcome)
        )

    if section_id == 0:

        return queryset.count()

    else:
        return queryset.filter(problem__problem_group__section__id=section_id).count()
