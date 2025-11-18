from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.appointments.models import DoctorAvailability
from apps.accounts.models import UserProfile
from datetime import time


class Command(BaseCommand):
    help = 'Setup default availability for all doctors'

    def handle(self, *args, **options):
        # Get all doctors
        doctors = User.objects.filter(userprofile__role='doctor', is_active=True)
        
        if not doctors.exists():
            self.stdout.write(
                self.style.WARNING('No doctors found. Please create doctor accounts first.')
            )
            return
        
        # Default availability schedule (Monday to Friday, 9 AM to 5 PM)
        default_schedule = [
            (0, time(9, 0), time(17, 0)),  # Monday
            (1, time(9, 0), time(17, 0)),  # Tuesday
            (2, time(9, 0), time(17, 0)),  # Wednesday
            (3, time(9, 0), time(17, 0)),  # Thursday
            (4, time(9, 0), time(17, 0)),  # Friday
        ]
        
        created_count = 0
        
        for doctor in doctors:
            for day_of_week, start_time, end_time in default_schedule:
                availability, created = DoctorAvailability.objects.get_or_create(
                    doctor=doctor,
                    day_of_week=day_of_week,
                    start_time=start_time,
                    defaults={
                        'end_time': end_time,
                        'is_active': True
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        f'Created availability for Dr. {doctor.get_full_name()} - '
                        f'{availability.get_day_of_week_display()} {start_time}-{end_time}'
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} availability slots for {doctors.count()} doctors.'
            )
        )
