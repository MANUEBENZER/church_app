from django.urls import path
#from .views import HomeView
from . import views
from .views import  *
from django.urls import include
from django.contrib.auth import views as auth_views



#app_name = 'members'



#urlpatterns = [
#    path('attendance/add/', views.add_attendance, name='add_attendance'),
#   path('attendance/', views.attendance_list, name='attendance_list'),
#    path('attendance/ajax_mark/', views.ajax_mark_attendance, name='ajax_mark_attendance'),
#    path('dashboard/', views.post_login_redirect, name='dashboard'),
#    path('export/attendance/excel/', views.export_attendance_excel, name='export_attendance_excel'),
#    path('export/attendance/pdf/', views.export_attendance_pdf, name='export_attendance_pdf'),
#    path('attendance/toggle/',views.ajax_toggle_attendance, name='ajax_toggle_attendance'),
#    path('attendance/chart-data/', views.attendance_chart_data, name='attendance_chart_data'),
#    path('attendance/export/excel/',views.export_attendance_excel, name='export_attendance_excel'),
#    path("", views.home, name = "home"),
#    path("redirect/", views.post_login_redirect, name = "post_login_redirect"),
#    path('dashboard/', views.dashboard, name='dashboard'),
#    path("secretary/dashboard", SecretaryDashboardView.as_view(), name='secretary_dashboard'),
#    path("secretary/announcements/", views.announcement_list, name="announcement_list"),
#    path("secretary/finance/", views.finance_dashboard, name="finance_dashboard"),
#    path("secretary/reports/", views.reports, name="reports"),
#    path("login/", auth_views.LoginView.as_view(
#        template_name="registration/login.html"
#    ), name="login"),
#
#    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
#    #path("admin/dashboard/", views.AdminDashboardView.as_view(), name="admin_dashboard"),
#    path("secretary/dashboard/", views.SecretaryDashboardView.as_view(), name="secretary_dashboard"),
#    path("pastor/dashboard/", views.PastorDashboardView.as_view(), name="pastor_dashboard"),
#    path("members/", views.member_list, name="member_list"),
#    path("<int:pk>/", views.member_detail, name="member_detail"),
#    path("<int:pk>/edit/", views.member_edit, name="member_edit"),
#    path("<int:pk>/delete/", views.member_delete, name="member_delete"),
#    path("add/", views.member_create, name="member_create"),
#    path("secretary/secretary_settings/", views.secretary_settings, name="secretary_settings"),
#    path("members/", member_list, name="member_list"),
#    path("members/<int:pk>/", member_detail, name="member_detail"),
#    path("members/export/excel/", export_members_excel, name="export_members_excel"),
#    path("members/export/pdf/", export_members_pdf, name="export_members_pdf"),
#]



app_name = 'members'  # ← important for namespaces

urlpatterns = [
    # Authentication
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Home & dashboard
    path("", views.home, name="home"),
    path("redirect/", views.post_login_redirect, name="post_login_redirect"),
    path("dashboard/", views.post_login_redirect, name='dashboard'),
    path("secretary/dashboard/", views.SecretaryDashboardView.as_view(), name="secretary_dashboard"),
    path("pastor/dashboard/", views.PastorDashboardView.as_view(), name="pastor_dashboard"),

    # Members
    path("members/", views.member_list, name="member_list"),
    path("members/add/", views.member_create, name="member_create"),
    path("members/<int:pk>/", views.member_detail, name="member_detail"),
    path("members/<int:pk>/edit/", views.member_edit, name="member_edit"),
    path("members/<int:pk>/delete/", views.member_delete, name="member_delete"),
    path("members/export/excel/", views.export_members_excel, name="export_members_excel"),
    path("members/export/pdf/", views.export_members_pdf, name="export_members_pdf"),

    # Attendance
    path("add_attendance/", views.add_attendance, name="add_attendance"),
    path("attendance/", views.attendance_list, name="attendance_list"),
   # path("attendance/ajax_mark/", views.ajax_mark_attendance, name="ajax_mark_attendance"),
    path("attendance/toggle/", views.ajax_toggle_attendance, name="ajax_toggle_attendance"),
    path("attendance/chart-data/", views.attendance_chart_data, name="attendance_chart_data"),
    path("export/attendance/excel/", views.export_attendance_excel, name="export_attendance_excel"),
    path("export/attendance/pdf/", views.export_attendance_pdf, name="export_attendance_pdf"),

    # Secretary
    path("secretary/finance/", views.finance_dashboard, name="finance_dashboard"),
    path("secretary/reports/", views.reports, name="reports"),
    path("secretary/secretary_settings/", views.secretary_settings, name="secretary_settings"),
    path("secretary/dashboard/",views.SecretaryDashboardView.as_view(),
    name="secretary_dashboard"),
    path("ajax/mark-attendance/", views.ajax_mark_attendance, name="ajax_mark_attendance"),
    path("announcements/announcements_dashboard/",views.announcements_dashboard,name="announcements_dashboard"),

]