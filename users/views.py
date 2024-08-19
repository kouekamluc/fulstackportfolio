
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Skill, Experience, Education, Testimonial, ReadingActivity

class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

class UserLoginView(LoginView):
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.next_page)
class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        # Get top tags
        context['top_tags'] = user.get_top_tags()

        # Calculate reading streak and total reading days
        reading_activities = ReadingActivity.objects.filter(user=user).order_by('date')
        if reading_activities.exists():
            streak = 1
            max_streak = 1
            prev_date = reading_activities.first().date
            for activity in reading_activities[1:]:
                if (activity.date - prev_date).days == 1:
                    streak += 1
                    max_streak = max(max_streak, streak)
                else:
                    streak = 1
                prev_date = activity.date
            
            user.longest_streak = max_streak
            user.total_reading_days = reading_activities.values('date').distinct().count()
            user.save()

        # Calculate posts read in the last year
        one_year_ago = timezone.now().date() - timedelta(days=365)
        context['posts_read_last_year'] = ReadingActivity.objects.filter(
            user=user,
            date__gte=one_year_ago
        ).count()

        # Get skills, experiences, education, and testimonials
        context['skills'] = Skill.objects.filter(user=user)
        context['experiences'] = Experience.objects.filter(user=user)
        context['education'] = Education.objects.filter(user=user)
        context['testimonials'] = Testimonial.objects.filter(user=user)

        return context

class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user