from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.utils import timezone
from django.urls import reverse

timezone.now()
class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)
    tags = TaggableManager()
    created_at = models.DateTimeField(default=timezone.now)  # Add this line
    
    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/')
    caption = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return f"Image for {self.project.title}"