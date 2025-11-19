from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Appointment, DoctorAvailability


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'appointment_type', 'reason', 'duration_minutes']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'min': timezone.now().date().strftime('%Y-%m-%d')
            }),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter doctors to only show users with doctor role
        doctors = User.objects.filter(userprofile__role='doctor', is_active=True)
        self.fields['doctor'].queryset = doctors
        self.fields['doctor'].empty_label = "Select a doctor"
        
        # Make reason optional with placeholder
        self.fields['reason'].required = False
        self.fields['reason'].widget.attrs['placeholder'] = 'Describe your symptoms or reason for visit (optional)'
        
        # Make duration_minutes optional with default
        self.fields['duration_minutes'].required = False
        self.fields['duration_minutes'].initial = 30
        
        # Add clinic CSS classes
        for field_name, field in self.fields.items():
            if field_name == 'reason':
                field.widget.attrs.update({
                    'class': 'clinic-input w-full px-4 py-3 rounded-xl resize-none'
                })
            else:
                field.widget.attrs.update({
                    'class': 'clinic-input w-full px-4 py-3 rounded-xl'
                })
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        doctor = cleaned_data.get('doctor')
        
        if date and time and doctor:
            # Check if appointment is in the past
            appointment_datetime = timezone.datetime.combine(date, time)
            # Make the datetime timezone-aware
            appointment_datetime = timezone.make_aware(appointment_datetime)
            if appointment_datetime < timezone.now():
                raise forms.ValidationError("Cannot schedule appointments in the past.")
            
            # Check if doctor is available at this time
            day_of_week = date.weekday()
            availability = DoctorAvailability.objects.filter(
                doctor=doctor,
                day_of_week=day_of_week,
                start_time__lte=time,
                end_time__gt=time,
                is_active=True
            ).exists()
            
            # If no availability is set, create default availability (9 AM to 5 PM on weekdays)
            if not availability and day_of_week < 5:  # Monday to Friday
                from datetime import time as dt_time
                # Create default availability for this doctor if none exists
                if not DoctorAvailability.objects.filter(doctor=doctor, day_of_week=day_of_week).exists():
                    DoctorAvailability.objects.create(
                        doctor=doctor,
                        day_of_week=day_of_week,
                        start_time=dt_time(9, 0),
                        end_time=dt_time(17, 0),
                        is_active=True
                    )
                    # Check again after creating default availability
                    availability = DoctorAvailability.objects.filter(
                        doctor=doctor,
                        day_of_week=day_of_week,
                        start_time__lte=time,
                        end_time__gt=time,
                        is_active=True
                    ).exists()
            
            if not availability:
                if day_of_week >= 5:  # Weekend
                    raise forms.ValidationError(f"Dr. {doctor.get_full_name()} is not available on weekends. Please select a weekday.")
                else:
                    raise forms.ValidationError(f"Dr. {doctor.get_full_name()} is not available at this time. Available hours are 9:00 AM to 5:00 PM on weekdays.")
            
            # Check for conflicting appointments (same doctor, date, time)
            existing_appointment = Appointment.objects.filter(
                doctor=doctor,
                date=date,
                time=time,
                status__in=['pending', 'approved']  # Only check non-cancelled appointments
            ).exclude(pk=self.instance.pk if self.instance else None).exists()
            
            if existing_appointment:
                # Get available times for this doctor on this date
                from datetime import time as dt_time, timedelta
                available_times = []
                doctor_availability = DoctorAvailability.objects.filter(
                    doctor=doctor,
                    day_of_week=day_of_week,
                    is_active=True
                ).first()
                
                if doctor_availability:
                    # Generate time slots (30-minute intervals)
                    current_time = doctor_availability.start_time
                    end_time = doctor_availability.end_time
                    
                    while current_time < end_time:
                        # Check if this time slot is available
                        slot_taken = Appointment.objects.filter(
                            doctor=doctor,
                            date=date,
                            time=current_time,
                            status__in=['pending', 'approved']
                        ).exists()
                        
                        if not slot_taken:
                            available_times.append(current_time.strftime('%H:%M'))
                        
                        # Add 30 minutes
                        current_datetime = timezone.datetime.combine(date, current_time)
                        current_datetime += timedelta(minutes=30)
                        current_time = current_datetime.time()
                        
                        if len(available_times) >= 5:  # Limit to first 5 available slots
                            break
                
                if available_times:
                    raise forms.ValidationError(f"This time slot is already booked with Dr. {doctor.get_full_name()}. Available times today: {', '.join(available_times)}")
                else:
                    raise forms.ValidationError(f"Dr. {doctor.get_full_name()} has no available slots on {date}. Please choose a different date.")
        
        return cleaned_data
    
    def save(self, commit=True):
        appointment = super().save(commit=False)
        
        # Only set patient if not already set and user is provided
        if not appointment.patient and self.user:
            appointment.patient = self.user
        
        # Set default values if not provided
        if not appointment.reason:
            appointment.reason = 'General consultation'
        if not appointment.duration_minutes:
            appointment.duration_minutes = 30
            
        if commit:
            appointment.save()
        return appointment


class DoctorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = ['day_of_week', 'start_time', 'end_time', 'is_active']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add clinic CSS classes
        for field_name, field in self.fields.items():
            if field_name == 'is_active':
                field.widget.attrs.update({
                    'class': 'rounded border-blue-200 text-blue-600 focus:ring-blue-300'
                })
            else:
                field.widget.attrs.update({
                    'class': 'clinic-select w-full px-4 py-3 rounded-xl'
                })
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("End time must be after start time.")
        
        return cleaned_data


class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status', 'notes', 'diagnosis', 'prescription', 'follow_up_instructions']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'General notes'}),
            'diagnosis': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Medical diagnosis'}),
            'prescription': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Medications and dosage'}),
            'follow_up_instructions': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Follow-up instructions'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            if field_name in ['notes', 'diagnosis', 'prescription', 'follow_up_instructions']:
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-rose-200 rounded-xl focus:ring-2 focus:ring-rose-500 resize-none'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-3 border border-rose-200 rounded-xl focus:ring-2 focus:ring-rose-500'
                })


class DoctorAppointmentActionForm(forms.Form):
    action = forms.ChoiceField(choices=[('approve', 'Approve'), ('decline', 'Decline')])
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional notes'}), required=False)
