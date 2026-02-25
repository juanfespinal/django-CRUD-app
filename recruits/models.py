from django.db import models
from django.utils import timezone


class Department(models.Model):
    """Department within the cleaning company"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Departments"
        ordering = ['name']

    def __str__(self):
        return self.name


class Position(models.Model):
    """Job position/opening"""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('filled', 'Filled'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='positions')
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    required_experience = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.location}"


class Candidate(models.Model):
    """Job candidate/applicant"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, related_name='candidates')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    experience_years = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Recruitment timeline tracking
    screening_date = models.DateTimeField(null=True, blank=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    offer_date = models.DateTimeField(null=True, blank=True)
    hired_date = models.DateTimeField(null=True, blank=True)
    rejected_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def time_to_hire(self):
        """Calculate days from application to hire"""
        if self.hired_date and self.applied_date:
            return (self.hired_date - self.applied_date).days
        return None

    @property
    def time_to_screening(self):
        """Calculate days from application to screening"""
        if self.screening_date and self.applied_date:
            return (self.screening_date - self.applied_date).days
        return None

    @property
    def time_to_interview(self):
        """Calculate days from application to interview stage"""
        if self.interview_date and self.applied_date:
            return (self.interview_date - self.applied_date).days
        return None

    @property
    def time_to_offer(self):
        """Calculate days from application to offer"""
        if self.offer_date and self.applied_date:
            return (self.offer_date - self.applied_date).days
        return None

    def update_status_timestamp(self, new_status):
        """Update the appropriate timestamp when status changes"""
        now = timezone.now()
        if new_status == 'screening' and not self.screening_date:
            self.screening_date = now
        elif new_status == 'interview' and not self.interview_date:
            self.interview_date = now
        elif new_status == 'offer' and not self.offer_date:
            self.offer_date = now
        elif new_status == 'hired' and not self.hired_date:
            self.hired_date = now
        elif new_status == 'rejected' and not self.rejected_date:
            self.rejected_date = now


class Interview(models.Model):
    """Interview scheduled with a candidate"""
    TYPE_CHOICES = [
        ('phone', 'Phone'),
        ('video', 'Video'),
        ('in_person', 'In-Person'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No-Show'),
    ]

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='interviews')
    interviewer_name = models.CharField(max_length=200)
    interviewer_email = models.EmailField(blank=True)
    scheduled_date = models.DateTimeField()
    scheduled_time = models.TimeField()
    interview_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='phone')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True)  # 1-5 rating
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['scheduled_date', 'scheduled_time']

    def __str__(self):
        return f"{self.candidate} - {self.scheduled_date}"
