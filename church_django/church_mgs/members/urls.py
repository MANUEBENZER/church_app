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
        path('promise/<int:promise_id>/edit/', views.edit_promise, name='edit_promise'),
        path('promise/<int:promise_id>/delete/', views.delete_promise, name='delete_promise'),
    # Authentication
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Home & dashboard
    path("", views.home, name="home"),
    path("redirect/", views.post_login_redirect, name="post_login_redirect"),
    path("dashboard/", views.post_login_redirect, name='dashboard'),
    #path("secretary/dashboard/", views.SecretaryDashboardView.as_view(), name="secretary_dashboard"),
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
   # path("announcements/add_attendance/", views.add_attendance, name="add_attendance"),
    path("add_attendance/", views.attendance_list, name="attendance_list"),
    path("attendance/ajax_mark/", views.ajax_mark_attendance, name="ajax_mark_attendance"),
    path("attendance/toggle/", views.ajax_toggle_attendance, name="ajax_toggle_attendance"),
    path("attendance/chart-data/", views.attendance_chart_data, name="attendance_chart_data"),
    path("export/attendance/excel/", views.export_attendance_excel, name="export_attendance_excel"),
    path("export/attendance/pdf/", views.export_attendance_pdf, name="export_attendance_pdf"),

    # Secretary
    path("secretary/finance/", views.finance_dashboard, name="finance_dashboard"),
    path("secretary/reports/", views.reports, name="reports"),
    path("secretary/secretary_settings/", views.secretary_settings, name="secretary_settings"),
    #path("secretary/dashboard/",views.SecretaryDashboardView.as_view(),name="secretary_dashboard"),
    path("secretary/secretary_dashboard/", views.secretary_dashboard, name="secretary_dashboard"),
    path("ajax/mark-attendance/", views.ajax_mark_attendance, name="ajax_mark_attendance"),
    path("announcements/promises_dashboard/",views.promises_dashboard,name="promises_dashboard"),
    path('announcements/add/', views.add_announcement, name='add_announcement'),
    path('attendance/add_attendance/', views.add_attendance, name='add_attendance'),
    path('promise/add/', views.add_promise, name='add_promise'),
    path("announcements/", views.announcement_dashboard, name="announcement_dashboard"),
    path("announcements/display/", views.announcement_display, name="announcement_display"),
    path("announcements/edit/<int:pk>/", views.announcement_edit, name="announcement_edit"),
    path("announcements/delete/<int:pk>/", views.announcement_delete, name="announcement_delete"),
    path("announcements/export/pdf/", views.export_announcements_pdf, name="export_announcements_pdf"),
    path("announcements/add_announcement/", views.add_announcement, name="add_announcement"),
    path("announcements/slide_show/", views.announcement_slide_show, name="announcement_slide_show"),
    path("announcements/add_promise/", views.add_promise, name="add_promise"),
    path("announcements/export/pdf/", views.export_promises_pdf, name="export_promises_pdf"),
    path("announcements/export/excel/", views.export_promises_excel, name="export_promises_excel"),
    path("finance/tithes_dashboard/", views.tithes_dashboard, name="tithes_dashboard"),
    path("finance/finance_home/", views.finance_home, name="finance_home"),

    #path('tithes/', views.tithes_records, name='tithes_records'),
    path('tithes/add/', views.add_tithe, name='add_tithe'),
    path('tithes/edit/<int:pk>/', views.edit_tithe, name='edit_tithe'),
    path('tithes/delete/<int:pk>/', views.delete_tithe, name='delete_tithe'),
    path('tithes/pdf/', views.tithes_pdf, name='tithes_pdf'),
    
]   