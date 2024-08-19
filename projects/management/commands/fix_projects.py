from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()

class Command(BaseCommand):
    help = 'Assigns a default user to all projects without a user'

    def handle(self, *args, **options):
        default_user, created = User.objects.get_or_create(username='default_user')
        if created:
            default_user.set_password('defaultpassword123')  # Set a password for the new user
            default_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created default user: {default_user.username}'))
        
        projects_updated = Project.objects.filter(user__isnull=True).update(user=default_user)
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {projects_updated} projects'))