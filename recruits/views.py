from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta, date
from .models import Candidate, Position, Interview, Department
import json


def landing_page(request):
    """Public landing page for marketing the app"""
    # Get some stats to display
    total_candidates = Candidate.objects.count()
    active_positions = Position.objects.filter(status='open').count()
    total_departments = Department.objects.count()
    
    context = {
        'total_candidates': total_candidates,
        'active_positions': active_positions,
        'total_departments': total_departments,
    }
    return render(request, 'landing.html', context)


def dashboard(request):
    """Main dashboard view with key metrics"""
    total_candidates = Candidate.objects.count()
    active_positions = Position.objects.filter(status='open').count()
    
    # Interviews this week
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=7)
    interviews_this_week = Interview.objects.filter(
        scheduled_date__gte=week_start,
        scheduled_date__lt=week_end
    ).count()
    
    # Hire rate
    total_completed = Candidate.objects.filter(status__in=['hired', 'rejected']).count()
    hired = Candidate.objects.filter(status='hired').count()
    hire_rate = round((hired / total_completed * 100), 1) if total_completed > 0 else 0
    
    # Candidates by status
    candidates_by_status = Candidate.objects.values('status').annotate(count=Count('id'))
    
    # Recent candidates
    recent_candidates = Candidate.objects.all()[:5]
    
    # Recent interviews
    recent_interviews = Interview.objects.select_related('candidate').order_by('-scheduled_date')[:5]
    
    context = {
        'total_candidates': total_candidates,
        'active_positions': active_positions,
        'interviews_this_week': interviews_this_week,
        'hire_rate': hire_rate,
        'candidates_by_status': list(candidates_by_status),
        'recent_candidates': recent_candidates,
        'recent_interviews': recent_interviews,
    }
    return render(request, 'dashboard.html', context)


def analytics(request):
    """Detailed analytics view"""
    # Candidates by status
    status_data = Candidate.objects.values('status').annotate(count=Count('id'))

    # Applications over time (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    applications_by_day = Candidate.objects.filter(
        applied_date__gte=thirty_days_ago
    ).extra(
        select={'day': "date(applied_date)"}
    ).values('day').annotate(count=Count('id')).order_by('day')

    # Hire rate by month (last 6 months)
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_hires = Candidate.objects.filter(
        status='hired',
        hired_date__gte=six_months_ago
    ).extra(
        select={'month': "strftime('%%Y-%%m', hired_date)"}
    ).values('month').annotate(count=Count('id')).order_by('month')

    # Positions by department
    positions_by_dept = Position.objects.values('department__name').annotate(
        count=Count('id')
    ).exclude(department__name__isnull=True)

    # Interview success rate
    completed_interviews = Interview.objects.filter(status='completed').count()
    no_shows = Interview.objects.filter(status='no_show').count()
    interview_show_rate = round((completed_interviews / (completed_interviews + no_shows) * 100), 1) if (completed_interviews + no_shows) > 0 else 0

    # Average interview rating
    avg_rating = Interview.objects.filter(rating__isnull=False).aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else 0

    # Metrics
    total_candidates = Candidate.objects.count()
    total_positions = Position.objects.count()
    open_positions = Position.objects.filter(status='open').count()
    total_interviews = Interview.objects.count()
    completed_interviews = Interview.objects.filter(status='completed').count()
    hired_candidates = Candidate.objects.filter(status='hired').count()

    # ==================== RECRUITMENT EFFICIENCY METRICS ====================

    # Average Time-to-Hire (days from application to hired)
    hired_with_dates = Candidate.objects.filter(
        status='hired',
        hired_date__isnull=False
    )
    avg_time_to_hire = None
    if hired_with_dates.exists():
        total_days = sum(
            (c.hired_date - c.applied_date).days
            for c in hired_with_dates
        )
        avg_time_to_hire = round(total_days / hired_with_dates.count(), 1)

    # Average Time-to-Screen (days from application to screening)
    screened = Candidate.objects.filter(screening_date__isnull=False)
    avg_time_to_screen = None
    if screened.exists():
        total_days = sum(
            (c.screening_date - c.applied_date).days
            for c in screened
        )
        avg_time_to_screen = round(total_days / screened.count(), 1)

    # Average Time-to-Interview (days from application to interview)
    interviewed = Candidate.objects.filter(interview_date__isnull=False)
    avg_time_to_interview = None
    if interviewed.exists():
        total_days = sum(
            (c.interview_date - c.applied_date).days
            for c in interviewed
        )
        avg_time_to_interview = round(total_days / interviewed.count(), 1)

    # Average Time-to-Offer (days from application to offer)
    offered = Candidate.objects.filter(offer_date__isnull=False)
    avg_time_to_offer = None
    if offered.exists():
        total_days = sum(
            (c.offer_date - c.applied_date).days
            for c in offered
        )
        avg_time_to_offer = round(total_days / offered.count(), 1)

    # Pipeline Conversion Rates
    total_screening = Candidate.objects.exclude(screening_date__isnull=True).count()
    total_interview = Candidate.objects.exclude(interview_date__isnull=True).count()
    total_offer = Candidate.objects.exclude(offer_date__isnull=True).count()
    total_hired = Candidate.objects.filter(status='hired').count()

    # Conversion rates
    screen_rate = round((total_screening / total_candidates * 100), 1) if total_candidates > 0 else 0
    interview_rate = round((total_interview / total_candidates * 100), 1) if total_candidates > 0 else 0
    offer_rate = round((total_offer / total_candidates * 100), 1) if total_candidates > 0 else 0
    hire_rate = round((total_hired / total_candidates * 100), 1) if total_candidates > 0 else 0

    # Pipeline velocity (candidates processed last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    weekly_screened = Candidate.objects.filter(screening_date__gte=seven_days_ago).count()
    weekly_interviewed = Candidate.objects.filter(interview_date__gte=seven_days_ago).count()
    weekly_offered = Candidate.objects.filter(offer_date__gte=seven_days_ago).count()
    weekly_hired = Candidate.objects.filter(hired_date__gte=seven_days_ago).count()

    # Stage duration data for funnel chart
    stage_data = [
        {'stage': 'Applied', 'count': total_candidates},
        {'stage': 'Screening', 'count': total_screening},
        {'stage': 'Interview', 'count': total_interview},
        {'stage': 'Offer', 'count': total_offer},
        {'stage': 'Hired', 'count': total_hired},
    ]

    context = {
        'status_data': list(status_data),
        'applications_by_day': list(applications_by_day),
        'monthly_hires': list(monthly_hires),
        'positions_by_dept': list(positions_by_dept),
        'interview_show_rate': interview_show_rate,
        'avg_rating': avg_rating,
        'total_candidates': total_candidates,
        'total_positions': total_positions,
        'open_positions': open_positions,
        'total_interviews': total_interviews,
        'completed_interviews': completed_interviews,
        'hired_candidates': hired_candidates,
        # Recruitment efficiency metrics
        'avg_time_to_hire': avg_time_to_hire,
        'avg_time_to_screen': avg_time_to_screen,
        'avg_time_to_interview': avg_time_to_interview,
        'avg_time_to_offer': avg_time_to_offer,
        'screen_rate': screen_rate,
        'interview_rate': interview_rate,
        'offer_rate': offer_rate,
        'hire_rate': hire_rate,
        'weekly_screened': weekly_screened,
        'weekly_interviewed': weekly_interviewed,
        'weekly_offered': weekly_offered,
        'weekly_hired': weekly_hired,
        'stage_data': stage_data,
    }
    return render(request, 'analytics.html', context)


# ==================== CANDIDATE VIEWS ====================

def candidate_list(request):
    """List all candidates with search and filter"""
    candidates = Candidate.objects.select_related('position').all()
    
    # Search
    search = request.GET.get('search', '')
    if search:
        candidates = candidates.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        candidates = candidates.filter(status=status_filter)
    
    # Filter by position
    position_filter = request.GET.get('position', '')
    if position_filter:
        candidates = candidates.filter(position_id=position_filter)
    
    # Pagination
    paginator = Paginator(candidates, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    positions = Position.objects.filter(status='open')
    statuses = Candidate.STATUS_CHOICES
    
    context = {
        'page_obj': page_obj,
        'positions': positions,
        'statuses': statuses,
        'search': search,
        'status_filter': status_filter,
        'position_filter': position_filter,
    }
    return render(request, 'candidates/list.html', context)


def candidate_create(request):
    """Create a new candidate"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        position_id = request.POST.get('position')
        status = request.POST.get('status', 'new')
        experience_years = request.POST.get('experience_years', 0)
        notes = request.POST.get('notes', '')

        position = Position.objects.get(id=position_id) if position_id else None

        candidate = Candidate(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            position=position,
            status=status,
            experience_years=experience_years,
            notes=notes
        )
        # Track initial status timestamp
        candidate.update_status_timestamp(status)
        candidate.save()

        messages.success(request, f'Candidate {candidate.full_name} created successfully!')

        if request.htmx:
            return render(request, 'components/toast.html', {
                'message': f'Candidate {candidate.full_name} created successfully!',
                'type': 'success'
            })

        return redirect('candidate_list')

    positions = Position.objects.filter(status='open')
    statuses = Candidate.STATUS_CHOICES

    if request.htmx:
        return render(request, 'candidates/form.html', {
            'candidate': None,
            'positions': positions,
            'statuses': statuses
        })

    return redirect('candidate_list')


def candidate_update(request, pk):
    """Update an existing candidate"""
    candidate = get_object_or_404(Candidate, pk=pk)

    if request.method == 'POST':
        candidate.first_name = request.POST.get('first_name')
        candidate.last_name = request.POST.get('last_name')
        candidate.email = request.POST.get('email')
        candidate.phone = request.POST.get('phone')
        candidate.position_id = request.POST.get('position') or None
        new_status = request.POST.get('status')
        # Track status change timestamp
        if new_status != candidate.status:
            candidate.update_status_timestamp(new_status)
        candidate.status = new_status
        candidate.experience_years = request.POST.get('experience_years', 0)
        candidate.notes = request.POST.get('notes', '')
        candidate.save()

        messages.success(request, f'Candidate {candidate.full_name} updated successfully!')

        if request.htmx:
            return render(request, 'components/toast.html', {
                'message': f'Candidate {candidate.full_name} updated successfully!',
                'type': 'success'
            })

        return redirect('candidate_list')

    positions = Position.objects.filter(status='open')
    statuses = Candidate.STATUS_CHOICES

    if request.htmx:
        return render(request, 'candidates/form.html', {
            'candidate': candidate,
            'positions': positions,
            'statuses': statuses
        })

    return redirect('candidate_list')


def candidate_delete(request, pk):
    """Delete a candidate"""
    if request.method == 'DELETE' or request.method == 'POST':
        candidate = get_object_or_404(Candidate, pk=pk)
        name = candidate.full_name
        candidate.delete()

        messages.success(request, f'Candidate {name} deleted successfully!')

        if request.htmx:
            return render(request, 'components/toast.html', {
                'message': f'Candidate {name} deleted successfully!',
                'type': 'success'
            })

    return redirect('candidate_list')


# ==================== POSITION VIEWS ====================

def position_list(request):
    """List all positions with search and filter"""
    positions = Position.objects.select_related('department').all()
    
    # Search
    search = request.GET.get('search', '')
    if search:
        positions = positions.filter(
            Q(title__icontains=search) |
            Q(location__icontains=search) |
            Q(department__name__icontains=search)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        positions = positions.filter(status=status_filter)
    
    # Filter by department
    dept_filter = request.GET.get('department', '')
    if dept_filter:
        positions = positions.filter(department_id=dept_filter)
    
    # Pagination
    paginator = Paginator(positions, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    departments = Department.objects.all()
    statuses = Position.STATUS_CHOICES
    
    context = {
        'page_obj': page_obj,
        'departments': departments,
        'statuses': statuses,
        'search': search,
        'status_filter': status_filter,
        'dept_filter': dept_filter,
    }
    return render(request, 'positions/list.html', context)


def position_create(request):
    """Create a new position"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        department_id = request.POST.get('department')
        location = request.POST.get('location')
        status = request.POST.get('status', 'open')
        salary_min = request.POST.get('salary_min')
        salary_max = request.POST.get('salary_max')
        required_experience = request.POST.get('required_experience', 0)

        department = Department.objects.get(id=department_id) if department_id else None

        position = Position.objects.create(
            title=title,
            description=description,
            department=department,
            location=location,
            status=status,
            salary_min=salary_min if salary_min else None,
            salary_max=salary_max if salary_max else None,
            required_experience=required_experience
        )

        messages.success(request, f'Position "{position.title}" created successfully!')

        if request.htmx:
            return render(request, 'components/toast.html', {
                'message': f'Position "{position.title}" created successfully!',
                'type': 'success'
            })

        return redirect('position_list')

    departments = Department.objects.all()
    statuses = Position.STATUS_CHOICES

    if request.htmx:
        return render(request, 'positions/form.html', {
            'position': None,
            'departments': departments,
            'statuses': statuses
        })

    return redirect('position_list')


def position_update(request, pk):
    """Update an existing position"""
    position = get_object_or_404(Position, pk=pk)

    if request.method == 'POST':
        position.title = request.POST.get('title')
        position.description = request.POST.get('description', '')
        position.department_id = request.POST.get('department') or None
        position.location = request.POST.get('location')
        position.status = request.POST.get('status')
        position.salary_min = request.POST.get('salary_min') or None
        position.salary_max = request.POST.get('salary_max') or None
        position.required_experience = request.POST.get('required_experience', 0)
        position.save()

        messages.success(request, f'Position "{position.title}" updated successfully!')

        if request.htmx:
            return render(request, 'components/toast.html', {
                'message': f'Position "{position.title}" updated successfully!',
                'type': 'success'
            })

        return redirect('position_list')

    departments = Department.objects.all()
    statuses = Position.STATUS_CHOICES

    if request.htmx:
        return render(request, 'positions/form.html', {
            'position': position,
            'departments': departments,
            'statuses': statuses
        })

    return redirect('position_list')


def position_delete(request, pk):
    """Delete a position"""
    if request.method == 'DELETE' or request.method == 'POST':
        position = get_object_or_404(Position, pk=pk)
        title = position.title
        position.delete()

        messages.success(request, f'Position "{title}" deleted successfully!')

        if request.htmx:
            return render(request, 'components/toast.html', {
                'message': f'Position "{title}" deleted successfully!',
                'type': 'success'
            })

    return redirect('position_list')


# ==================== INTERVIEW VIEWS ====================

def interview_list(request):
    """List all interviews with search and filter"""
    interviews = Interview.objects.select_related('candidate', 'candidate__position').all()
    
    # Search
    search = request.GET.get('search', '')
    if search:
        interviews = interviews.filter(
            Q(candidate__first_name__icontains=search) |
            Q(candidate__last_name__icontains=search) |
            Q(interviewer_name__icontains=search)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        interviews = interviews.filter(status=status_filter)
    
    # Filter by type
    type_filter = request.GET.get('type', '')
    if type_filter:
        interviews = interviews.filter(interview_type=type_filter)
    
    # Filter by date range
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if date_from:
        interviews = interviews.filter(scheduled_date__gte=date_from)
    if date_to:
        interviews = interviews.filter(scheduled_date__lte=date_to)
    
    # Pagination
    paginator = Paginator(interviews, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    candidates = Candidate.objects.all()
    statuses = Interview.STATUS_CHOICES
    types = Interview.TYPE_CHOICES
    
    context = {
        'page_obj': page_obj,
        'candidates': candidates,
        'statuses': statuses,
        'types': types,
        'search': search,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'interviews/list.html', context)


def interview_create(request):
    """Create a new interview"""
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate')
        interviewer_name = request.POST.get('interviewer_name')
        interviewer_email = request.POST.get('interviewer_email', '')
        scheduled_date = request.POST.get('scheduled_date')
        scheduled_time = request.POST.get('scheduled_time')
        interview_type = request.POST.get('interview_type', 'phone')
        status = request.POST.get('status', 'scheduled')
        notes = request.POST.get('notes', '')
        rating = request.POST.get('rating')

        candidate = Candidate.objects.get(id=candidate_id)

        interview = Interview.objects.create(
            candidate=candidate,
            interviewer_name=interviewer_name,
            interviewer_email=interviewer_email,
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time,
            interview_type=interview_type,
            status=status,
            notes=notes,
            rating=rating if rating else None
        )

        messages.success(request, f'Interview scheduled for {interview.candidate.full_name}!')

        if request.htmx:
            return render(request, 'components/toast.html', {
                'message': f'Interview scheduled for {interview.candidate.full_name}!',
                'type': 'success'
            })

        return redirect('interview_list')

    candidates = Candidate.objects.filter(status__in=['new', 'screening', 'interview'])
    statuses = Interview.STATUS_CHOICES
    types = Interview.TYPE_CHOICES

    if request.htmx:
        return render(request, 'interviews/form.html', {
            'interview': None,
            'candidates': candidates,
            'statuses': statuses,
            'types': types
        })

    return redirect('interview_list')


def interview_update(request, pk):
    """Update an existing interview"""
    interview = get_object_or_404(Interview, pk=pk)

    if request.method == 'POST':
        interview.candidate_id = request.POST.get('candidate')
        interview.interviewer_name = request.POST.get('interviewer_name')
        interview.interviewer_email = request.POST.get('interviewer_email', '')
        interview.scheduled_date = request.POST.get('scheduled_date')
        interview.scheduled_time = request.POST.get('scheduled_time')
        interview.interview_type = request.POST.get('interview_type')
        interview.status = request.POST.get('status')
        interview.notes = request.POST.get('notes', '')
        interview.rating = request.POST.get('rating') or None
        interview.save()

        messages.success(request, f'Interview updated successfully!')

        if request.htmx:
            return render(request, 'components/toast.html', {
                'message': 'Interview updated successfully!',
                'type': 'success'
            })

        return redirect('interview_list')

    candidates = Candidate.objects.all()
    statuses = Interview.STATUS_CHOICES
    types = Interview.TYPE_CHOICES

    if request.htmx:
        return render(request, 'interviews/form.html', {
            'interview': interview,
            'candidates': candidates,
            'statuses': statuses,
            'types': types
        })

    return redirect('interview_list')


def interview_delete(request, pk):
    """Delete an interview"""
    if request.method == 'DELETE' or request.method == 'POST':
        interview = get_object_or_404(Interview, pk=pk)
        candidate_name = interview.candidate.full_name
        interview.delete()

        messages.success(request, f'Interview with {candidate_name} deleted!')

        if request.htmx:
            return render(request, 'components/toast.html', {
                'message': f'Interview with {candidate_name} deleted!',
                'type': 'success'
            })

    return redirect('interview_list')


# ==================== DEPARTMENT VIEWS ====================

def department_create(request):
    """Create a new department"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')

        department = Department.objects.create(
            name=name,
            description=description
        )

        messages.success(request, f'Department "{department.name}" created!')

        if request.htmx:
            return render(request, 'components/toast.html', {
                'message': f'Department "{department.name}" created!',
                'type': 'success'
            })

    return redirect('position_list')
