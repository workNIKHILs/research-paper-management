from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Publication, Faculty
from .forms import LoginForm, FacultyRegisterForm, PublicationForm
import datetime


# --- Auth ---
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, f"Welcome back, {form.get_user().username}!")
        return redirect('dashboard')
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')


def register_view(request):
    form = FacultyRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        Faculty.objects.create(
            user=user,
            name=form.cleaned_data['name'],
            designation=form.cleaned_data['designation'],
            department=form.cleaned_data['department'],
            joining_date=form.cleaned_data['joining_date'],
        )
        messages.success(request, "Account created! Please login.")
        return redirect('login')
    return render(request, 'core/register.html', {'form': form})


# --- Dashboard ---
@login_required
def dashboard(request):
    if request.user.is_superuser:
        pubs = Publication.objects.all()
    else:
        pubs = Publication.objects.filter(faculty__user=request.user)

    context = {
        'total': pubs.count(),
        'journals': pubs.filter(type='journal').count(),
        'conferences': pubs.filter(type='conference').count(),
        'books': pubs.filter(type='book').count(),
        'book_chapters': pubs.filter(type='book_chapter').count(),
        'recent': pubs.order_by('-created_at')[:5],
    }
    return render(request, 'core/dashboard.html', context)


# --- Upload ---
@login_required
def upload_publication(request):
    form = PublicationForm(request.POST or None, request.FILES or None)

    # Non-admin faculty can only upload for themselves
    if not request.user.is_superuser:
        form.fields['faculty'].queryset = Faculty.objects.filter(
            user=request.user
        )
        form.fields['faculty'].initial = request.user.faculty

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "✅ Publication uploaded successfully!")
        return redirect('publication_list')
    elif request.method == 'POST':
        messages.error(request, "❌ Please fix the errors below.")

    return render(request, 'core/upload.html', {'form': form})


# --- List & Filter ---
@login_required
def publication_list(request):
    if request.user.is_superuser:
        pubs = Publication.objects.all()
    else:
        pubs = Publication.objects.filter(faculty__user=request.user)

    # Filters
    search      = request.GET.get('search', '')
    pub_type    = request.GET.get('type', '')
    faculty_id  = request.GET.get('faculty', '')
    department  = request.GET.get('department', '')
    designation = request.GET.get('designation', '')
    year        = request.GET.get('year', '')
    month       = request.GET.get('month', '')

    if search:
        pubs = pubs.filter(
            Q(title__icontains=search) |
            Q(faculty__name__icontains=search) |
            Q(journal_name__icontains=search) |
            Q(conference_name__icontains=search)
        )
    if pub_type:
        pubs = pubs.filter(type=pub_type)
    if faculty_id:
        pubs = pubs.filter(faculty__id=faculty_id)
    if department:
        pubs = pubs.filter(faculty__department=department)
    if designation:
        pubs = pubs.filter(faculty__designation=designation)
    if year:
        pubs = pubs.filter(year=year)
    if month:
        pubs = pubs.filter(month=month)

    years = Publication.objects.values_list(
        'year', flat=True
    ).distinct().order_by('-year')

    context = {
        'publications': pubs.order_by('-year', '-month'),
        'faculties': Faculty.objects.all(),
        'years': years,
        'filters': request.GET,
    }
    return render(request, 'core/publications.html', context)