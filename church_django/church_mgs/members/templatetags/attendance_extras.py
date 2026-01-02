from django import template

register = template.Library()

@register.filter
def latest_attendance(attendance_qs, service):
    return attendance_qs.filter(service=service).order_by('-date').first()
