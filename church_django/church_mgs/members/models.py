from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Member(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    DEPARTMENT_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Youth', 'Youth'),
        ('Children', 'Children'),
        ('Choir', 'Choir'),
        ('Ushering', 'Ushering'),
    ]

    POSITION_CHOICES = [
        ('Member', 'Member'),
        ('Elder', 'Elder'),
        ('Deacon', 'Deacon'),
        ('Pastor', 'Pastor'),
        ('Worker', 'Worker'),
    ]

    # 🔹 Basic Info
    membership_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='members/', null=True, blank=True)
    class Meta:
            ordering = ["full_name"]
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.photo:
            img = Image.open(self.photo.path)

            # Force square crop
            width, height = img.size
            min_dim = min(width, height)

            left = (width - min_dim) / 2
            top = (height - min_dim) / 2
            right = (width + min_dim) / 2
            bottom = (height + min_dim) / 2

            img = img.crop((left, top, right, bottom))
            img = img.resize((150, 150), Image.Resampling.LANCZOS)

            img.save(self.photo.path)

    # 🔹 Church Info
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, default='Member')
    date_joined = models.DateField(auto_now_add=True)
    baptized = models.BooleanField(default=False)

    # 🔹 Contact Info
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True)
    

    
    # 🔹 Status
    is_active = models.BooleanField(default=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_members"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.membership_id})"

    def attendance_count(self):
        return self.attendance_set.filter(present=True).count()
    def attendance_percentage(self):
        total = self.attendance_set.count()
        if total == 0:
            return 0
        present = self.attendance_set.filter(present=True).count()
        return round((present / total) * 100, 1)
    

class Profile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Pastor', 'Pastor'),
        ('Member', 'Member'),
        ('Secretary','Secretary'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
        


class Attendance(models.Model):
    SERVICE_CHOICES = [
        ('Sunday', 'Sunday Service'),
        ('Midweek', 'Midweek Service'),
        ('Prayers', 'Prayers'),
        ('Prayer Meeting', 'Prayer Meeting'),
        ('Bible Study', 'Bible Study'),
        ('Intercessory Prayer', 'Intercessory Prayer'),
        ('Special Prayer Campaign', 'Special Prayer Campaign'),
        ('Youth Prayer Gathering', 'Youth Prayer Gathering'),
        ('Prayer and Testimony', 'Prayer and Testimony'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=150, choices=SERVICE_CHOICES)
    date = models.DateField()
    present = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["member", "date", "service_type"],
                name="unique_member_attendance_per_service"
            )
        ]
    def __str__(self):
        return f"{self.member.full_name} - {self.service_type} ({self.date})"


#class Attendance(models.Model):
#    ...
#    locked = models.BooleanField(default=False)
class DailyChurchReport(models.Model):
    SERVICE_CHOICES = [
        ('Sunday', 'Sunday Service'),
        ('Midweek', 'Midweek Service'),
        ('Prayers', 'Prayers'),
        ('Prayer Meeting', 'Prayer Meeting'),
        ('Bible Study', 'Bible Study'),
        ('Intercessory Prayer', 'Intercessory Prayer'),
        ('Special Prayer Campaign', 'Special Prayer Campaign'),
        ('Youth Prayer Gathering', 'Youth Prayer Gathering'),
        ('Prayer and Testimony', 'Prayer and Testimony'),
    ]

    date = models.DateField(unique=True)
    service_type = models.CharField(max_length=30, choices=SERVICE_CHOICES)

    announcements = models.TextField()
    total_attendance = models.PositiveIntegerField()
    men = models.PositiveIntegerField(default=0)
    women = models.PositiveIntegerField(default=0)
    children = models.PositiveIntegerField(default=0)

    offering_amount = models.DecimalField(max_digits=10, decimal_places=2)
    promises_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    special_notes = models.TextField(blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} - {self.service_type}"




class Promise(models.Model):
    fulfilled = models.BooleanField(default=False, help_text="Mark as fulfilled when promise is completed")
    PROMISE_TYPE_CHOICES = (
        ('money', 'Money'),
        ('item', 'Item'),
    )

    report = models.ForeignKey(
        DailyChurchReport,
        on_delete=models.CASCADE,
        related_name='promises'
    )
    member_name = models.CharField(max_length=150)
    promise_type = models.CharField(max_length=10, choices=PROMISE_TYPE_CHOICES)

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    item_description = models.CharField(max_length=255, blank=True)

    # ✅ NEW FIELD
    due_date = models.DateField(
        null=True, blank=True,
        help_text="Date the member promised to bring the item or money"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member_name} - {self.promise_type}"



class Income(models.Model):
    INCOME_TYPE_CHOICES = [
        ("tithe", "Tithe"),
        ("annual_harvest", "Annual Harvest"),
        ("ntintam", "Ntintam"),
        ("thanksgiving", "Thanksgiving"),
        ("donation", "Donation"),
        ("offering", "Offering"),
        ("other", "Other"),
    ]

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    income_type = models.CharField(max_length=30, choices=INCOME_TYPE_CHOICES)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['income_type']),
        ]
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.get_income_type_display()} - {self.amount} on {self.date}"

    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than zero")
# Church Expense Model
class Expense(models.Model):
    EXPENSE_CATEGORY_CHOICES = [
        ("utilities", "Utilities"),
        ("maintenance", "Maintenance"),
        ("salary", "Salary"),
        ("event", "Event"),
        ("charity", "Charity"),
        ("supplies", "Supplies"),
        ("other", "Other"),
    ]
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=30, choices=EXPENSE_CATEGORY_CHOICES)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.get_category_display()} - {self.amount} on {self.date}"
# Church Income Model




class Announcement(models.Model):
    title = models.CharField(max_length=150)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)
    display_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title