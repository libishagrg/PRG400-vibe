from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()


class Command(BaseCommand):
    help = 'Create superuser from environment variables if one does not exist'

    def handle(self, *args, **options):
        email = config('DJANGO_SUPERUSER_EMAIL', default='admin@travel.com')
        password = config('DJANGO_SUPERUSER_PASSWORD', default='admin123')
        username = config('DJANGO_SUPERUSER_USERNAME', default='admin')

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser created: {email}'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser already exists: {email}'))
