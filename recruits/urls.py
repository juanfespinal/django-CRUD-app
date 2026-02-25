from django.urls import path
from . import views

urlpatterns = [
    # Landing Page (public)
    path('landing/', views.landing_page, name='landing_page'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Analytics
    path('analytics/', views.analytics, name='analytics'),
    
    # Candidates
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('candidates/create/', views.candidate_create, name='candidate_create'),
    path('candidates/<int:pk>/edit/', views.candidate_update, name='candidate_update'),
    path('candidates/<int:pk>/delete/', views.candidate_delete, name='candidate_delete'),
    
    # Positions
    path('positions/', views.position_list, name='position_list'),
    path('positions/create/', views.position_create, name='position_create'),
    path('positions/<int:pk>/edit/', views.position_update, name='position_update'),
    path('positions/<int:pk>/delete/', views.position_delete, name='position_delete'),
    
    # Interviews
    path('interviews/', views.interview_list, name='interview_list'),
    path('interviews/create/', views.interview_create, name='interview_create'),
    path('interviews/<int:pk>/edit/', views.interview_update, name='interview_update'),
    path('interviews/<int:pk>/delete/', views.interview_delete, name='interview_delete'),
    
    # Departments
    path('departments/create/', views.department_create, name='department_create'),
]
