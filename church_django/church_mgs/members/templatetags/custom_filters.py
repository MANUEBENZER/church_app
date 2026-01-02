from django import template

register = template.Library()

@register.filter
def full_name(member):
    return f"{member.first_name} {member.last_name}"



@register.filter
def latest_attendance(attendance_qs, service):
    return attendance_qs.filter(service_type=service).order_by('-date').first()




@register.filter
def mul(value, arg):
    try:
        return int(value) * int(arg)
    except Exception:
        return 0

@register.filter
def div(value, arg):
    try:
        return round(int(value) / int(arg), 1)
    except Exception:
        return 0