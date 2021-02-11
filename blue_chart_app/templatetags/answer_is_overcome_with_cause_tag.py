from django import template
from blue_chart_app.models.connect import Connect
from django.core.exceptions import ObjectDoesNotExist


register = template.Library()

@register.simple_tag
def answer_is_overcome_with_cause_tag(answer_id, cause_tag_id):

    try:
        connect = Connect.objects.get(
            answer__id=answer_id, cause_tag__id=cause_tag_id
        )
        if connect.is_overcome:
            return "克服"
        else:
            return "未克服"

    except ObjectDoesNotExist:
            
        return "-"

