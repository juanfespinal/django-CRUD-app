from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # Landing Page (public)
    path('', views.landing_page, name='home'),
    path('landing/', views.landing_page, name='landing_page'),
    
    # Dashboard
    path('dashboard/', login_required(views.dashboard), name='dashboard'),
    
    # Analytics
    path('analytics/', login_required(views.analytics), name='analytics'),
    
    # Candidates
    path('candidates/', login_required(views.candidate_list), name='candidate_list'),
    path('candidates/create/', login_required(views.candidate_create), name='candidate_create'),
    path('candidates/<int:pk>/edit/', login_required(views.candidate_update), name='candidate_update'),
    path('candidates/<int:pk>/delete/', login_required(views.candidate_delete), name='candidate_delete'),
    
    # Positions
    path('positions/', login_required(views.position_list), name='position_list'),
    path('positions/create/', login_required(views.position_create), name='position_create'),
    path('positions/<int:pk>/edit/', login_required(views.position_update), name='position_update'),
    path('positions/<int:pk>/delete/', login_required(views.position_delete), name='position_delete'),
    
    # Interviews
    path('interviews/', login_required(views.interview_list), name='interview_list'),
    path('interviews/create/', login_required(views.interview_create), name='interview_create'),
    path('interviews/<int:pk>/edit/', login_required(views.interview_update), name='interview_update'),
    path('interviews/<int:pk>/delete/', login_required(views.interview_delete), name='interview_delete'),
    
    # Departments
    path('departments/create/', login_required(views.department_create), name='department_create'),
]
