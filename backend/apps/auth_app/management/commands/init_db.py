from django.core.management.base import BaseCommand
from apps.auth_app.models import User

class Command(BaseCommand):
    help = 'Initialize database with test users'
    
    def handle(self, *args, **options):
        # Create admin user if not exists
        if not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_user(
                email='admin@example.com',
                password='Admin123!',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        
        # Create test employee users
        for i in range(1, 4):
            if not User.objects.filter(email=f'employee{i}@example.com').exists():
                User.objects.create_user(
                    email=f'employee{i}@example.com',
                    password='Employee123!',
                    role='employee'
                )
                self.stdout.write(self.style.SUCCESS(f'Employee {i} created'))
        
        self.stdout.write(self.style.SUCCESS('Database initialization complete'))