from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView

from .forms import RegisterForm, LoginForm, EnquiryForm, AppointmentForm, AppointmentStatusForm
from .models import Appointment, TattooStyle, Artist, Studio, Review, Enquiry



# ============================================
# PUBLIC LANDING PAGE (NO LOGIN REQUIRED)
# ============================================

def landing_page(request):
    """Public landing page - Homepage"""
    styles = TattooStyle.objects.filter(is_active=True)[:4]
    artists = Artist.objects.filter(is_active=True)[:8]
    studios = Studio.objects.filter(is_active=True)[:2]
    reviews = Review.objects.filter(is_approved=True, is_featured=True)[:4]
    
    context = {
        'styles': styles,
        'artists': artists,
        'studios': studios,
        'reviews': reviews,
    }
    return render(request, 'appointments/landing.html', context)


def enquiry_submit(request):
    """Handle tattoo enquiry form submission"""
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✨ Thank you for your enquiry! We\'ll get back to you within 24 hours. 💀')
            return redirect('appointments:landing')
        else:
            messages.error(request, 'Please correct the errors in the form.')
            return redirect('appointments:landing')
    return redirect('appointments:landing')


# ============================================
# AUTHENTICATION VIEWS (Login appears first)
# ============================================

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('appointments:index')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}! 💀')
                
                # Redirect to 'next' parameter or default based on role
                default_redirect = 'appointments:manage' if user.is_staff else 'appointments:index'
                next_url = request.GET.get('next') or default_redirect
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'appointments/login.html', {'form': form})

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('appointments:index')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('appointments:landing')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    
    return render(request, 'appointments/register.html', {'form': form})

def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('appointments:login')

# ============================================
# PROTECTED VIEWS (Require login)
# ============================================

@login_required(login_url='appointments:login')
def index(request):
    """Tattoo-inspired dashboard after login"""
    base_queryset = Appointment.objects.all() if request.user.is_staff else Appointment.objects.filter(user=request.user)
    now = timezone.now()

    upcoming_appointments = base_queryset.filter(appointment_date__gte=now).order_by('appointment_date')[:5]
    recent_activity = base_queryset.order_by('-created_at')[:4]

    stats = {
        'total': base_queryset.count(),
        'pending': base_queryset.filter(status='pending').count(),
        'approved': base_queryset.filter(status='approved').count(),
        'rejected': base_queryset.filter(status='rejected').count(),
        'next_session': upcoming_appointments[0].appointment_date if upcoming_appointments else None,
    }

    context = {
        'upcoming_appointments': upcoming_appointments,
        'recent_activity': recent_activity,
        'stats': stats,
        'show_all': request.user.is_staff,
    }
    return render(request, 'appointments/index.html', context)


@login_required(login_url='appointments:login')
def appointment_create(request):
    """Allow authenticated clients to request appointments"""
    if request.user.is_staff:
        return redirect('appointments:manage')

    if request.method == 'POST':
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            if timezone.is_naive(appointment.appointment_date):
                appointment.appointment_date = timezone.make_aware(
                    appointment.appointment_date,
                    timezone.get_current_timezone()
                )
            appointment.status = 'pending'
            appointment.save()
            messages.success(request, 'Appointment submitted! We will review and get back to you.')
            return redirect('appointments:index')
        messages.error(request, 'Please correct the errors below.')
    else:
        initial = {
            'client_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }
        form = AppointmentForm(initial=initial)

    return render(request, 'appointments/create_appointment.html', {'form': form})


def staff_check(user):
    return user.is_staff


@user_passes_test(staff_check, login_url='appointments:login')
def manage_appointments(request):
    appointments = Appointment.objects.all().order_by('-created_at')
    status_form = AppointmentStatusForm()
    return render(
        request,
        'appointments/manage.html',
        {
            'appointments': appointments,
            'status_form': status_form,
        }
    )


@user_passes_test(staff_check, login_url='appointments:login')
def update_appointment_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, f"Appointment for {appointment.client_name} marked as {appointment.get_status_display()}.")
        else:
            messages.error(request, 'Invalid status update.')
    return redirect('appointments:manage')

@login_required(login_url='appointments:login')
def appointment_list_fbv(request):
    """Function-Based View (FBV) - Protected"""
    if request.user.is_staff:
        appointments = Appointment.objects.all()
        view_type = 'Function-Based View (FBV)'
    else:
        appointments = Appointment.objects.filter(user=request.user)
        view_type = 'My Appointments (FBV)'
    context = {
        'appointments': appointments,
        'view_type': view_type
    }
    return render(request, 'appointments/appointment_list.html', context)

class AppointmentListCBV(LoginRequiredMixin, ListView):
    """Class-Based View (CBV) - Protected"""
    login_url = 'appointments:login'
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = 'Class-Based View (CBV)' if self.request.user.is_staff else 'My Appointments (CBV)'
        return context

# ============================================
# EDIT AND DELETE VIEWS
# ============================================

@login_required(login_url='appointments:login')
def appointment_edit(request, pk):
    """Edit an appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        appointment.client_name = request.POST.get('client_name')
        appointment.email = request.POST.get('email')
        appointment.phone = request.POST.get('phone')
        appointment.tattoo_design = request.POST.get('tattoo_design')
        appointment.appointment_date = request.POST.get('appointment_date')
        appointment.save()
        
        messages.success(request, f'Appointment for {appointment.client_name} updated successfully! 💀')
        return redirect('appointments:list-fbv')
    
    return render(request, 'appointments/edit.html', {'appointment': appointment})

@login_required(login_url='appointments:login')
def appointment_delete(request, pk):
    """Delete an appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        client_name = appointment.client_name
        appointment.delete()
        messages.success(request, f'Appointment for {client_name} has been deleted. 💀')
        return redirect('appointments:list-fbv')
    
    return render(request, 'appointments/delete_confirm.html', {'appointment': appointment})