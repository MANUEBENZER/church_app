
from django.contrib import admin
from .models import Member
from .models import Profile
from django.urls import reverse
from django.utils.html import format_html



admin.site.register(Profile)
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('membership_id', 'full_name', 'department', 'phone', 'is_active')
    search_fields = ('full_name', 'membership_id', 'phone')
    list_filter = ('department', 'gender', 'is_active')


admin.site.site_header = "Church Management System"
admin.site.site_title = "Church Admin"
admin.site.index_title = "Administration"

def dashboard_link(obj):
    url = reverse("secretary_dashboard")
    return format_html('<a href="{}">Secretary Dashboard</a>', url)

# Register your models here.
