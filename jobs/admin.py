from django.contrib import admin
from .models import Freelancer, Job, Application


@admin.register(Freelancer)
class FreelancerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "skills", "created_at")
    search_fields = ("full_name", "email", "skills")
    list_filter = ("created_at",)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "required_skills", "posted_at")
    search_fields = ("title", "required_skills")
    list_filter = ("posted_at",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "freelancer", "job", "status", "applied_at")
    search_fields = ("freelancer__full_name", "job__title", "status")
    list_filter = ("status", "applied_at")
