from django import template

register = template.Library()

@register.filter(name="latest_attendance")
def latest_attendance(attendance_queryset, service_name):
    return (
        attendance_queryset
        .filter(service_type=service_name)
        .order_by("-date")
        .first()
    )
