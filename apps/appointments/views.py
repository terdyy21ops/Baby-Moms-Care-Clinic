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
        'page_obj': page_obj,
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
                appointment = form.save()
                
                # Create notification for doctor
                Notification.objects.create(
                    user=appointment.doctor,
                    title='New Appointment Booked',
                    message=f'{appointment.patient.get_full_name()} has booked an appointment for {appointment.date} at {appointment.time}.',
                    notification_type='appointment'
                )
                
                messages.success(request, 'Appointment booked successfully!')
                return redirect('appointments:detail', pk=appointment.pk)
            except Exception as e:
                messages.error(request, f'Error creating appointment: {str(e)}')
                # Add more detailed error information for debugging
                import traceback
                messages.error(request, f'Debug info: {traceback.format_exc()}')
        else:
            # Add form errors to messages for debugging
            messages.error(request, 'Please correct the following errors:')
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
                    status__in=['scheduled', 'confirmed']
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
