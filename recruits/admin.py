from django.contrib import admin
from .models import Department, Position, Candidate, Interview


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'location', 'status', 'created_at']
    list_filter = ['status', 'department', 'location']
    search_fields = ['title', 'description', 'location']
    list_editable = ['status']


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'position', 'status', 'experience_years', 'applied_date']
    list_filter = ['status', 'position', 'applied_date']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_editable = ['status']
    readonly_fields = ['applied_date', 'updated_at']


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'interviewer_name', 'scheduled_date', 'interview_type', 'status', 'rating']
    list_filter = ['status', 'interview_type', 'scheduled_date']
    search_fields = ['candidate__first_name', 'candidate__last_name', 'interviewer_name']
    list_editable = ['status', 'rating']
    readonly_fields = ['created_at', 'updated_at']
