from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Appointment, DoctorAvailability
from .forms import AppointmentForm, DoctorAvailabilityForm, AppointmentUpdateForm
from apps.accounts.models import UserProfile, Notification
from datetime import datetime, timedelta


@login_required
def appointment_list(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.role == 'mother':
        appointments = Appointment.objects.filter(patient=request.user)
    elif user_profile.role == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user)
    else:  # admin
        appointments = Appointment.objects.all()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        if user_profile.role == 'mother':
            appointments = appointments.filter(
                Q(doctor__first_name__icontains=search_query) |
                Q(doctor__last_name__icontains=search_query) |
                Q(reason__icontains=search_query)
            )
        else:
            appointments = appointments.filter(
                Q(patient__first_name__icontains=search_query) |
                Q(patient__last_name__icontains=search_query) |
                Q(reason__icontains=search_query)
            )
    
    appointments = appointments.order_by('-date', '-time')
    
    # Pagination
    paginator = Paginator(appointments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'appointments/list.html', {
        'appointments': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'user_profile': user_profile,
        'status_filter': status_filter,
        'search_query': search_query,
    })


@login_required
def appointment_create(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Only mothers can create appointments
    if user_profile.role != 'mother':
        messages.error(request, 'Only mothers can book appointments.')
        return redirect('appointments:list')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                appointment.patient = request.user
                appointment.save()
                
                # Create notification for doctor
                Notification.objects.create(
                    user=appointment.doctor,
                    title='New Appointment Booked',
                    message=f'{appointment.patient.get_full_name()} has booked an appointment for {appointment.date} at {appointment.time}.',
                    notification_type='appointment'
                )
                
                messages.success(request, f'Appointment booked successfully! Your appointment with Dr. {appointment.doctor.get_full_name()} is scheduled for {appointment.date} at {appointment.time}.')
                return redirect('appointments:list')
            except Exception as e:
                messages.error(request, f'Error creating appointment: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f'{error}')
                    else:
                        messages.error(request, f'{field.replace("_", " ").title()}: {error}')
    else:
        form = AppointmentForm(user=request.user)
    
    return render(request, 'appointments/create.html', {'form': form})


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Check permissions
    if user_profile.role == 'mother' and appointment.patient != request.user:
        messages.error(request, 'You can only view your own appointments.')
        return redirect('appointments:list')
    elif user_profile.role == 'doctor' and appointment.doctor != request.user:
        messages.error(request, 'You can only view your own appointments.')
        return redirect('appointments:list')
    
    return render(request, 'appointments/detail.html', {
        'appointment': appointment,
        'user_profile': user_profile,
    })


@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Check permissions
    if user_profile.role == 'mother':
        if appointment.patient != request.user:
            messages.error(request, 'You can only edit your own appointments.')
            return redirect('appointments:list')
        
        # Mothers can only edit if appointment is not in the past and not completed
        if appointment.is_past or appointment.status in ['completed', 'cancelled']:
            messages.error(request, 'Cannot edit past or completed appointments.')
            return redirect('appointments:detail', pk=pk)
        
        form_class = AppointmentForm
    elif user_profile.role == 'doctor':
        if appointment.doctor != request.user:
            messages.error(request, 'You can only edit your own appointments.')
            return redirect('appointments:list')
        
        form_class = AppointmentUpdateForm
    else:  # admin
        form_class = AppointmentUpdateForm
    
    if request.method == 'POST':
        if user_profile.role == 'mother':
            form = form_class(request.POST, instance=appointment, user=request.user)
        else:
            form = form_class(request.POST, instance=appointment)
        
        if form.is_valid():
            updated_appointment = form.save()
            
            # Create notification for relevant parties
            if user_profile.role == 'doctor' and 'status' in form.changed_data:
                Notification.objects.create(
                    user=updated_appointment.patient,
                    title='Appointment Status Updated',
                    message=f'Your appointment status has been updated to {updated_appointment.get_status_display()}.',
                    notification_type='appointment'
                )
            
            messages.success(request, 'Appointment updated successfully!')
            return redirect('appointments:detail', pk=pk)
    else:
        if user_profile.role == 'mother':
            form = form_class(instance=appointment, user=request.user)
        else:
            form = form_class(instance=appointment)
    
    return render(request, 'appointments/update.html', {
        'form': form,
        'appointment': appointment,
        'user_profile': user_profile,
    })


@login_required
def appointment_cancel(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Check permissions
    if user_profile.role == 'mother' and appointment.patient != request.user:
        messages.error(request, 'You can only cancel your own appointments.')
        return redirect('appointments:list')
    elif user_profile.role == 'doctor' and appointment.doctor != request.user:
        messages.error(request, 'You can only cancel your own appointments.')
        return redirect('appointments:list')
    
    if not appointment.can_be_cancelled:
        messages.error(request, 'This appointment cannot be cancelled.')
        return redirect('appointments:detail', pk=pk)
    
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        
        # Create notification for the other party
        if user_profile.role == 'mother':
            Notification.objects.create(
                user=appointment.doctor,
                title='Appointment Cancelled',
                message=f'{appointment.patient.get_full_name()} has cancelled the appointment scheduled for {appointment.date} at {appointment.time}.',
                notification_type='appointment'
            )
        else:
            Notification.objects.create(
                user=appointment.patient,
                title='Appointment Cancelled',
                message=f'Your appointment with Dr. {appointment.doctor.get_full_name()} scheduled for {appointment.date} at {appointment.time} has been cancelled.',
                notification_type='appointment'
            )
        
        messages.success(request, 'Appointment cancelled successfully!')
        return redirect('appointments:list')
    
    return render(request, 'appointments/cancel.html', {'appointment': appointment})


@login_required
def doctor_availability(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Only doctors can manage availability
    if user_profile.role != 'doctor':
        messages.error(request, 'Only doctors can manage availability.')
        return redirect('appointments:list')
    
    availabilities = DoctorAvailability.objects.filter(doctor=request.user).order_by('day_of_week', 'start_time')
    
    return render(request, 'appointments/availability.html', {
        'availabilities': availabilities
    })


@login_required
def availability_create(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.role != 'doctor':
        messages.error(request, 'Only doctors can set availability.')
        return redirect('appointments:list')
    
    if request.method == 'POST':
        form = DoctorAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.doctor = request.user
            availability.save()
            messages.success(request, 'Availability added successfully!')
            return redirect('appointments:availability')
    else:
        form = DoctorAvailabilityForm()
    
    return render(request, 'appointments/availability_form.html', {'form': form})


@login_required
def availability_update(request, pk):
    availability = get_object_or_404(DoctorAvailability, pk=pk, doctor=request.user)
    
    if request.method == 'POST':
        form = DoctorAvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            form.save()
            messages.success(request, 'Availability updated successfully!')
            return redirect('appointments:availability')
    else:
        form = DoctorAvailabilityForm(instance=availability)
    
    return render(request, 'appointments/availability_form.html', {'form': form, 'availability': availability})


@login_required
def availability_delete(request, pk):
    availability = get_object_or_404(DoctorAvailability, pk=pk, doctor=request.user)
    
    if request.method == 'POST':
        availability.delete()
        messages.success(request, 'Availability deleted successfully!')
        return redirect('appointments:availability')
    
    return render(request, 'appointments/availability_delete.html', {'availability': availability})


@login_required
def calendar_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.role == 'mother':
        appointments = Appointment.objects.filter(patient=request.user)
    elif user_profile.role == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user)
    else:  # admin
        appointments = Appointment.objects.all()
    
    # Filter by current month if no specific date range provided
    current_month = timezone.now().date().replace(day=1)
    appointments = appointments.filter(date__gte=current_month)
    
    # Get all active doctors for the calendar view
    doctors = User.objects.filter(userprofile__role='doctor', is_active=True).prefetch_related('availabilities')
    
    return render(request, 'appointments/calendar.html', {
        'appointments': appointments,
        'user_profile': user_profile,
        'doctors': doctors,
    })


@login_required
def check_availability(request):
    """AJAX view to check doctor availability for a specific date"""
    if request.method == 'GET':
        doctor_id = request.GET.get('doctor_id')
        date_str = request.GET.get('date')
        
        if not doctor_id or not date_str:
            return JsonResponse({'error': 'Missing doctor_id or date'}, status=400)
        
        try:
            from datetime import datetime, time as dt_time, timedelta
            doctor = User.objects.get(id=doctor_id, userprofile__role='doctor')
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            day_of_week = date.weekday()
            
            # Get doctor availability for this day
            availability = DoctorAvailability.objects.filter(
                doctor=doctor,
                day_of_week=day_of_week,
                is_active=True
            ).first()
            
            if not availability:
                # Create default availability if none exists
                if day_of_week < 5:  # Weekday
                    availability = DoctorAvailability.objects.create(
                        doctor=doctor,
                        day_of_week=day_of_week,
                        start_time=dt_time(9, 0),
                        end_time=dt_time(17, 0),
                        is_active=True
                    )
                else:
                    return JsonResponse({'available_times': [], 'message': 'Doctor not available on weekends'})
            
            # Generate available time slots
            available_times = []
            current_time = availability.start_time
            end_time = availability.end_time
            
            while current_time < end_time:
                # Check if this time slot is available
                slot_taken = Appointment.objects.filter(
                    doctor=doctor,
                    date=date,
                    time=current_time,
                    status__in=['pending', 'approved']
                ).exists()
                
                if not slot_taken:
                    available_times.append({
                        'time': current_time.strftime('%H:%M'),
                        'display': current_time.strftime('%I:%M %p')
                    })
                
                # Add 30 minutes
                current_datetime = timezone.datetime.combine(date, current_time)
                current_datetime += timedelta(minutes=30)
                current_time = current_datetime.time()
            
            return JsonResponse({
                'available_times': available_times,
                'doctor_name': doctor.get_full_name()
            })
            
        except User.DoesNotExist:
            return JsonResponse({'error': 'Doctor not found'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def doctor_directory(request):
    """View all available doctors with their profiles and availability"""
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Get all active doctors
    doctors = User.objects.filter(
        userprofile__role='doctor',
        is_active=True
    ).select_related('userprofile').prefetch_related('availabilities')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        doctors = doctors.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(userprofile__specialization__icontains=search_query)
        )
    
    # Filter by specialization
    specialization = request.GET.get('specialization')
    if specialization:
        doctors = doctors.filter(userprofile__specialization__icontains=specialization)
    
    return render(request, 'appointments/doctor_directory.html', {
        'doctors': doctors,
        'user_profile': user_profile,
        'search_query': search_query,
        'specialization': specialization,
    })


@login_required
def doctor_dashboard(request):
    """Enhanced doctor dashboard with appointment overview"""
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.role != 'doctor':
        messages.error(request, 'This page is only accessible to doctors.')
        return redirect('accounts:dashboard')
    
    today = timezone.now().date()
    
    # Get ALL appointments for this doctor
    all_appointments = Appointment.objects.filter(doctor=request.user).select_related('patient', 'patient__userprofile')
    
    # Today's appointments (all statuses)
    today_appointments = all_appointments.filter(date=today).order_by('time')
    
    # Upcoming appointments (future dates, pending or approved)
    upcoming_appointments = all_appointments.filter(
        date__gt=today,
        status__in=['pending', 'approved']
    ).order_by('date', 'time')[:5]
    
    # Pending approvals (all pending regardless of date)
    pending_appointments = all_appointments.filter(status='pending').count()
    
    # Completed today
    completed_today = all_appointments.filter(date=today, status='completed').count()
    
    # Total unique patients
    total_patients = all_appointments.values('patient').distinct().count()
    
    # Check if user is new (first login)
    is_new_user = request.user.last_login is None
    
    context = {
        'user_profile': user_profile,
        'today_appointments': today_appointments,
        'upcoming_appointments': upcoming_appointments,
        'pending_appointments': pending_appointments,
        'completed_today': completed_today,
        'total_patients': total_patients,
        'is_new_user': is_new_user,
    }
    
    return render(request, 'appointments/doctor_dashboard.html', context)


@login_required
def mother_dashboard(request):
    """Enhanced mother dashboard with appointment overview"""
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.role != 'mother':
        messages.error(request, 'This page is only accessible to mothers.')
        return redirect('accounts:dashboard')
    
    # Get appointments
    today = timezone.now().date()
    upcoming_appointments = Appointment.objects.filter(
        patient=request.user,
        date__gte=today,
        status__in=['pending', 'approved']
    ).order_by('date', 'time')[:5]
    
    recent_appointments = Appointment.objects.filter(
        patient=request.user,
        status='completed'
    ).order_by('-date', '-time')[:5]
    
    pending_appointments = Appointment.objects.filter(
        patient=request.user,
        status='pending'
    ).count()
    
    total_appointments = Appointment.objects.filter(patient=request.user).count()
    
    # Get available doctors count
    available_doctors = User.objects.filter(
        userprofile__role='doctor',
        is_active=True
    ).count()
    
    # Check if user is new (first login)
    is_new_user = request.user.last_login is None
    
    context = {
        'user_profile': user_profile,
        'upcoming_appointments': upcoming_appointments,
        'recent_appointments': recent_appointments,
        'pending_appointments': pending_appointments,
        'total_appointments': total_appointments,
        'available_doctors': available_doctors,
        'is_new_user': is_new_user,
    }
    
    return render(request, 'appointments/mother_dashboard.html', context)


@login_required
def doctor_appointment_action(request, pk, action):
    """Quick approve/decline/complete appointment"""
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.role != 'doctor':
        messages.error(request, 'Only doctors can perform this action.')
        return redirect('appointments:list')
    
    appointment = get_object_or_404(Appointment, pk=pk, doctor=request.user)
    
    if action == 'approve':
        appointment.status = 'approved'
        messages.success(request, f'Appointment with {appointment.patient.get_full_name()} approved successfully!')
        
        Notification.objects.create(
            user=appointment.patient,
            title='Appointment Approved',
            message=f'Your appointment on {appointment.date} at {appointment.time} has been approved by Dr. {appointment.doctor.get_full_name()}.',
            notification_type='appointment'
        )
    elif action == 'decline':
        appointment.status = 'cancelled'
        messages.success(request, 'Appointment declined.')
        
        Notification.objects.create(
            user=appointment.patient,
            title='Appointment Declined',
            message=f'Your appointment request for {appointment.date} at {appointment.time} was declined.',
            notification_type='appointment'
        )
    elif action == 'complete':
        appointment.status = 'completed'
        messages.success(request, f'Appointment with {appointment.patient.get_full_name()} marked as completed!')
        
        Notification.objects.create(
            user=appointment.patient,
            title='Appointment Completed',
            message=f'Your appointment on {appointment.date} has been completed. Check your medical records for details.',
            notification_type='appointment'
        )
    else:
        messages.error(request, 'Invalid action.')
        return redirect('appointments:detail', pk=pk)
    
    appointment.save()
    
    # Redirect back to dashboard or detail based on request
    if request.GET.get('from') == 'dashboard':
        return redirect('appointments:doctor_dashboard')
    return redirect('appointments:detail', pk=pk)


@login_required
def patient_records(request, patient_id):
    """View patient medical history"""
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.role != 'doctor':
        messages.error(request, 'Only doctors can view patient records.')
        return redirect('appointments:list')
    
    patient = get_object_or_404(User, id=patient_id)
    patient_profile = get_object_or_404(UserProfile, user=patient)
    
    # Get all appointments with this patient
    appointments = Appointment.objects.filter(
        doctor=request.user,
        patient=patient
    ).order_by('-date', '-time')
    
    context = {
        'patient': patient,
        'patient_profile': patient_profile,
        'appointments': appointments,
    }
    
    return render(request, 'appointments/patient_records.html', context)
