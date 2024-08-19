from django.contrib import admin
from .models import CustomUser , Skill, Experience, Education, Testimonial, ReadingActivity
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Skill)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Testimonial)
admin.site.register(ReadingActivity)