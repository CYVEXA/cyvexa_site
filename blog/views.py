from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Blog, Event
from .forms import BlogForm, EventForm
from django.shortcuts import render, get_object_or_404, redirect

# =========================
# 🔐 ROLE CHECK (ADMIN ONLY)
# =========================
def admin_only(user):
    return user.is_authenticated and user.is_staff


# =========================
# 🏠 INDEX PAGES (PUBLIC)
# =========================
def index(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'Services.html')

def works(request):
    return render(request, 'works.html')

def about(request):
    return render(request, 'Aboutus.html')

def contact(request):
    return render(request, 'contact.html')


# =========================
# 🔐 LOGIN (ADMIN + USERS CAN LOGIN)
# =========================
def user_login(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'registration/login.html')


# =========================
# 🚪 LOGOUT
# =========================
def user_logout(request):
    logout(request)
    return redirect('index')


# =========================
# 📝 BLOG (PUBLIC VIEW)
# =========================
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})


# CREATE BLOG (LOGIN REQUIRED)
@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogForm()

    return render(request, 'create_blog.html', {'form': form})


# EDIT BLOG (ADMIN ONLY OR OWNER)
@login_required
def edit_blog(request, id):
    blog = get_object_or_404(Blog, id=id)

    if request.user != blog.author and not request.user.is_staff:
        return redirect('blog_list')

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogForm(instance=blog)

    return render(request, 'edit_blog.html', {'form': form})


# DELETE BLOG
@login_required
def delete_blog(request, id):
    blog = get_object_or_404(Blog, id=id)

    if request.user != blog.author and not request.user.is_staff:
        return redirect('blog_list')

    if request.method == "POST":
        blog.delete()
        return redirect('blog_list')

    return render(request, 'delete_confirm.html', {'blog': blog})


from django.db.models import Q

# =========================
# 📅 EVENTS (PUBLIC VIEW)
# =========================
def event_list(request):
    today = timezone.now().date()

    # Query all events, newest/upcoming first
    events = Event.objects.all().order_by('-start_date')

    upcoming_events = Event.objects.filter(start_date__gt=today).order_by('start_date')
    ongoing_events = Event.objects.filter(
        Q(start_date__lte=today, end_date__gte=today) |
        Q(start_date=today, end_date__isnull=True)
    ).order_by('start_date')
    completed_events = Event.objects.filter(
        Q(end_date__lt=today) |
        Q(end_date__isnull=True, start_date__lt=today)
    ).order_by('-start_date')

    # Ordered unified list: ongoing, then upcoming, then completed
    ordered_events = list(ongoing_events) + list(upcoming_events) + list(completed_events)
    # If no categorized difference, fallback to all events
    if not ordered_events and events.exists():
        ordered_events = list(events)

    return render(request, 'events.html', {
        'events': ordered_events,
        'upcoming_events': upcoming_events,
        'ongoing_events': ongoing_events,
        'completed_events': completed_events,
        'total_count': events.count(),
        'upcoming_count': upcoming_events.count(),
        'ongoing_count': ongoing_events.count(),
        'completed_count': completed_events.count(),
    })


# =========================
# 🔐 EVENTS (ADMIN ONLY)
# =========================
@login_required
@user_passes_test(admin_only)
@login_required
@user_passes_test(admin_only)
def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()

    return render(request, 'blog/add_event.html', {'form': form})

@login_required
@user_passes_test(admin_only)
def edit_event(request, id):
    event = get_object_or_404(Event, id=id)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'blog/edit_event.html', {'form': form})


@login_required
@user_passes_test(admin_only)
def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    event.delete()
    return redirect('event_list')   # IMPORTANT