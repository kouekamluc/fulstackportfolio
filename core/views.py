
from django.views.generic import ListView
from django.db.models import Q
from itertools import chain
from operator import attrgetter
from projects.models import Project
from blog.models import Post  # Assuming you have a blog app with a Post model

class HomeView(ListView):
    template_name = 'core/home.html'
    context_object_name = 'feed_items'
    paginate_by = 10

    def get_queryset(self):
        projects = Project.objects.all()
        posts = Post.objects.filter(is_published=True)  # Assuming you have a 'published' field

        # Combine and sort projects and posts
        feed_items = sorted(
            chain(projects, posts),
            key=attrgetter('created_at'),
            reverse=True
        )

        return feed_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_items'] = [
            {
                'title': item.title,
                'description': item.description if hasattr(item, 'description') else item.content[:200],
                'author': item.user.username if hasattr(item, 'user') else item.author.username,
                'created_at': item.created_at,
                'type': 'project' if isinstance(item, Project) else 'article',
                'url': item.get_absolute_url(),
            }
            for item in context['feed_items']
        ]
        return context