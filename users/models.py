from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

from django.db.models import Count
from collections import Counter
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    
    # New fields for daily.dev-like profile
    reputation = models.IntegerField(default=0)
    profile_views = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    total_reading_days = models.IntegerField(default=0)
    posts_read_last_year = models.IntegerField(default=0)

   
    def get_top_tags(self):
        activities = self.reading_activities.all()
        all_tags = [tag for activity in activities for tag in activity.get_tags()]
        tag_counts = Counter(all_tags)
        total_count = sum(tag_counts.values())
        
        top_tags = [
            {'name': tag, 'percentage': int((count / total_count) * 100)}
            for tag, count in tag_counts.most_common(6)
        ]
        return top_tags

    def calculate_streak(self):
        activities = self.reading_activities.order_by('date')
        if not activities:
            return 0

        current_streak = 1
        max_streak = 1
        prev_date = activities[0].date

        for activity in activities[1:]:
            if (activity.date - prev_date).days == 1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
            prev_date = activity.date

        self.longest_streak = max_streak
        self.save()
        return max_streak

    def update_reading_stats(self):
        activities = self.reading_activities.all()
        self.total_reading_days = activities.values('date').distinct().count()
        self.posts_read_last_year = activities.filter(date__gte=timezone.now() - timezone.timedelta(days=365)).count()
        self.save()
        
        
class Skill(models.Model):
    user = models.ForeignKey(CustomUser,default=1, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

class Experience(models.Model):
    user = models.ForeignKey(CustomUser,default=1, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()

class Education(models.Model):
    user = models.ForeignKey(CustomUser,default=1, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

class Testimonial(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1,related_name='testimonials')
    author = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

User = get_user_model()


class ReadingActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1, related_name='reading_activities')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)  # Store tags as a comma-separated string

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        ordering = ['-date']

    def set_tags(self, tags):
        self.tags = ','.join(tags)

    def get_tags(self):
        return self.tags.split(',') if self.tags else []