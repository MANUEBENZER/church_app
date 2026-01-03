from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.db.models import Count,  Q
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from lxml.objectify import annotate
from xhtml2pdf import pisa
from datetime import timedelta
import openpyxl
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models  import Attendance, Member, DailyChurchReport, Promise
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from .utils import is_admin, is_secretary
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from django import forms
from datetime import date





@login_required
def post_login_redirect(request):
    user = request.user

    # Django Admin users
    if user.is_superuser or user.is_staff:
        return redirect("/admin/")

    if user.groups.filter(name="Secretary").exists():
        return redirect("members:secretary_dashboard")

    if user.groups.filter(name="Pastor").exists():
        return redirect("members:pastor_dashboard")

    # fallback
    return redirect("members:home")


class AttendanceDashboardView(TemplateView):
    template_name = 'attendance/secretary_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs = Attendance.objects.all()

        # Filters
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        service = self.request.GET.get('service')

        if start:
            qs = qs.filter(date__gte=start)
        if end:
            qs = qs.filter(date__lte=end)
        if service:
            qs = qs.filter(service=service)

        context['total'] = qs.count()
        context['present'] = qs.filter(present=True).count()
        context['absent'] = qs.filter(present=False).count()
        context['services'] = Attendance.objects.values_list('service', flat=True).distinct()

        return context


class PastorDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "pastor/secretary_dashboard.html"

    def test_func(self):
        return self.request.user.groups.filter(name="Pastor").exists()


from django.db.models.functions import TruncWeek, TruncMonth

weekly = (
    Attendance.objects
    .annotate(week=TruncWeek('date'))
    .values('week')
    .annotate(total=Count('id'))
)

monthly = (
    Attendance.objects
    .annotate(month=TruncMonth('date'))
    .values('month')
    .annotate(total=Count('id'))
)


@login_required
def announcements_dashboard(request):
    today = now().date()

    report, created = DailyChurchReport.objects.get_or_create(
        date=today,
        defaults={
            'service_type': 'Sunday',
            'announcements': '',
            'total_attendance': 0,
            'offering_amount': 0,
            'created_by': request.user
        }
    )

    # 🔹 AUTO-PULL attendance summary
    attendance_summary = Attendance.objects.filter(
        date=today,
        service_type=report.service_type
    ).aggregate(
        total_present=Count('id', filter=Q(present=True)),
        total_absent=Count('id', filter=Q(present=False)),
        total_members=Count('id')
    )

    # 🔹 Auto-fill attendance
    report.total_attendance = attendance_summary['total_present'] or 0
    report.save(update_fields=['total_attendance'])

    if request.method == "POST":
        # 🔹 Update report fields
        report.service_type = request.POST.get("service_type")
        report.announcements = request.POST.get("announcements")
        report.offering_amount = request.POST.get("offering_amount") or 0
        report.promises_amount = request.POST.get("promises_amount") or 0
        report.special_notes = request.POST.get("special_notes")
        report.created_by = request.user
        report.save()

        # 🔹 Get promise fields safely
        member_name = request.POST.get("promise_member")
        promise_type = request.POST.get("promise_type")
        amount = request.POST.get("promise_amount")
        item = request.POST.get("promise_item")
        due_date = request.POST.get("promise_due_date")

        # 🔹 Save promise only if filled
        if member_name and promise_type:
            Promise.objects.create(
                report=report,
                member_name=member_name,
                promise_type=promise_type,
                amount=amount if promise_type == "money" else None,
                item_description=item if promise_type == "item" else "",
                due_date=due_date or None
            )

        return redirect("members:announcements_dashboard")
    promises= Promise.objects.filter(report=report)
    return render(request, "announcements/announcements_dashboard.html", {
        "report": report,
        "today": today,
        "attendance_summary": attendance_summary,
        "promises": promises
    })


from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@user_passes_test(is_admin)
def delete_attendance(request, id):
    ...



def attendance_chart_data(request):
    qs = Attendance.objects.all()

    if request.GET.get('service'):
        qs = qs.filter(service=request.GET['service'])

    data = (
        qs.values('date')
        .annotate(present=Count('id', filter=Q(present=True)))
        .order_by('date')
    )

    return JsonResponse({
        'labels': [d['date'] for d in data],
        'present': [d['present'] for d in data]
    })

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_admin(self.request.user)


@require_POST
def ajax_toggle_attendance(request):
    attendance_id = request.POST.get('attendance_id')
    attendance = get_object_or_404(Attendance, id=attendance_id)

    attendance.present = not attendance.present
    attendance.save()

    return JsonResponse({
        'status': 'present' if attendance.present else 'absent'
    })
# -----------------------------
# Add Attendance (AJAX-friendly)
# -----------------------------
@login_required
def add_attendance(request):
    today = date.today()

    # Service type (default Sunday)
    service_type = request.GET.get("service", "Sunday")

    # Search query
    search_query = request.GET.get("q", "").strip()

    members = Member.objects.prefetch_related("attendance_set").filter(is_active=True)

    # ✅ FIXED SEARCH (matches your model)
    if search_query:
        members = members.filter(
            Q(full_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(membership_id__icontains=search_query)
        )

    for member in members:
        Attendance.objects.filter(
            member=member,
            date=today,
            service_type=service_type
        ).exists() or Attendance.objects.create(
            member=member,
            date=today,
            service_type=service_type,
            present=False
        )


    # Members already marked present today
    present_member_ids = Attendance.objects.filter(
        date=today,
        service_type=service_type,
        present=True
    ).values_list("member_id", flat=True)

    return render(request, "attendance/add_attendance.html", {
        "members": members,
        "service_type": service_type,
        "today": today,
        "present_member_ids": list(present_member_ids),
        "search_query": search_query,
    })


# -----------------------------
# AJAX Attendance Marking
# -----------------------------
def ajax_mark_attendance(request):
    if request.method == "POST":
        member_id = request.POST.get("member_id")
        service_type = request.POST.get("service_type")
        attendance_date = request.POST.get("date")
        present = request.POST.get("present") == "true"

        attendance, created = Attendance.objects.get_or_create(
            member_id=member_id,
            service_type=service_type,
            date=attendance_date,
            defaults={"present": present}
        )

        if not created:
            attendance.present = present
            attendance.save()

        return JsonResponse({
            "status": "ok",
            "present": attendance.present
        })
# -----------------------------
# Attendance List
# -----------------------------
#def attendance_list(request):
#    members = Member.objects.annotate(
#        total_attendance=Count('attendance'),
#        present_count=Count(
#            'attendance',
#            filter=Q(attendance__present=True)
#        )
#    )
#
#    return render(request, 'attendance/attendance_list.html', {
#        'members': members,
#    })
#def attendance_list(request):
 #   user = request.user
#
  #  if user.groups.filter(name="Secretary").exists():
#        base_template = "secretary/base.html"
#    elif user.groups.filter(name="Pastor").exists():
#        base_template = "pastor/base.html"
 #   elif user.is_superuser:
 #       base_template = "admin/base_site.html"
#    else:
#        base_template = "base.html"
#
 #   context = {
 #       "base_template": base_template,
 #       "members": members,
 #       "services": services,
 #   }
#
 #   return render(request, "attendance_list.html", context)



@login_required
def attendance_list(request):
    user = request.user

    if user.groups.filter(name="Secretary").exists():
        base_template = "secretary/base.html"
    elif user.groups.filter(name="Pastor").exists():
        base_template = "pastor/base.html"
    elif user.is_superuser:
        base_template = "admin/base_site.html"
    else:
        base_template = "base.html"

    members = Member.objects.annotate(
        total_attendance=Count('attendance'),
        present_count=Count(
            'attendance',
            filter=Q(attendance__present=True)
        )
    )

    # 🔹 Extract services from Attendance instead
    services = Attendance.objects.values_list(
        "service_type", flat=True
    ).distinct()

    context = {
        "base_template": base_template,
        "members": members,
        "services": services,
    }

    return render(request, "attendance/attendance_list.html", context)



# -----------------------------
# Dashboard
# -----------------------------
def dashboard(request):
    today = now().date()
    # Last 7 days
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    attendance_data = []
    for day in last_7_days:
        count = Attendance.objects.filter(date=day, present=True).count()
        attendance_data.append({'date': day.strftime('%Y-%m-%d'), 'count': count})

    total_members = Member.objects.count()
    present_today = Attendance.objects.filter(date=today, present=True).count()

    return render(request, 'secretary_dashboard.html', {
        'attendance_data': attendance_data,
        'total_members': total_members,
        'present_today': present_today,
    })




def export_members_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=church_members.pdf"

    p = canvas.Canvas(response)
    y = 800

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y, "Church Members List")
    y -= 40

    p.setFont("Helvetica", 10)

    for m in Member.objects.all():
        p.drawString(
            50, y,
            f"{m.membership_id} | {m.full_name} | {m.department} | {m.phone}"
        )
        y -= 18
        if y < 50:
            p.showPage()
            y = 800

    p.save()
    return response




def export_members_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append([
        "Membership ID", "Full Name", "Gender", "Department",
        "Position", "Phone", "Email", "Status"
    ])

    for m in Member.objects.all():
        ws.append([
            m.membership_id,
            m.full_name,
            m.gender,
            m.department,
            m.position,
            m.phone,
            m.email,
            "Active" if m.is_active else "Inactive"
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=church_members.xlsx"
    wb.save(response)
    return response


@login_required
@user_passes_test(is_secretary)
def member_create(request):
    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("members:member_list")
    else:
        form = MemberForm()
    return render(request, "members/create_member_form.html", {"form": form, "action": "Add"})

@login_required
@user_passes_test(is_secretary)
def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)

    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = request.user
            obj.save()
            return redirect("members:member_detail", pk=member.pk)
    else:
        form = MemberForm(instance=member)

    return render(request, "members/member_edit_detail.html", {
        "form": form,
        "member": member
    })

@login_required
#@user_passes_test(is_superuser)
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        member.delete()
        messages.success(request, "Member deleted successfully.")
        return redirect("members:member_list")
    # Optional: confirm page
    return render(request, "members/member_confirm_delete.html", {"member": member})





# -----------------------------
# Export Attendance to Excel
# -----------------------------
def export_attendance_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Attendance + {{Service.name}}+' ' +{{Date}}"

    # Header
    ws.append(["Member", "Service", "Date", "Present"])

    # Data
    for att in Attendance.objects.select_related('member').all():
        ws.append([
            f"{att.member.full_name} ",
            att.service_type,
            att.date.strftime('%Y-%m-%d'),
            "Yes" if att.present else "No"
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=attendance.xlsx'
    wb.save(response)
    return response


# -----------------------------
# Export Attendance to PDF
# -----------------------------
def export_attendance_pdf(request):
    template_path = 'attendance_pdf.html'
    attendances = Attendance.objects.select_related('member').all()
    context = {'attendances': attendances}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="attendance.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



class SecretaryDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "secretary/secretary_dashboard.html"

    def test_func(self):
        user = self.request.user
        return user.groups.filter(name="Secretary").exists()


def member_list(request):
    q = request.GET.get("q", "")
    members = Member.objects.filter(full_name__icontains=q) if q else Member.objects.all()

    paginator = Paginator(members, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "members/member_list.html", {
        "page_obj": page_obj
    })


@method_decorator(login_required, name="dispatch")
class SecretaryDashboardView(TemplateView):
    template_name = "secretary/secretary_dashboard.html"


@login_required
def announcement_list(request):
    return render(request, "members/secretary/announcement_list.html")


@login_required
def finance_dashboard(request):
    return render(request, "members/secretary/finance_dashboard.html")


@login_required
def reports(request):
    return render(request, "members/secretary/reports.html")

@login_required
def secretary_settings(request):
    return render(request, "members/secretary/secretary_settings.html")

@login_required
@user_passes_test(is_secretary)
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)

    attendance_summary = (
        Attendance.objects
        .filter(member=member, present=True)
        .values("service_type")
        .annotate(total=Count("id"))
    )

    total_attendance = Attendance.objects.filter(
        member=member, present=True
    ).count()

    return render(request, "members/member_detail.html", {
        "member": member,
        "attendance_count": total_attendance,
        "attendance_summary": attendance_summary
    })

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = "__all__"
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }



@login_required
@user_passes_test(is_secretary)
def member_create(request):
    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("member:member_list")
    else:
        form = MemberForm()

    return render(request, "members/create_member_form.html", {"form": form})






# -----------------------------
# Home Redirect
# -----------------------------
def home(request):
    return render(request, "home.html")


@login_required
def dashboard(request):
    return render(request, 'secretary_dashboard.html')