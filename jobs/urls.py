from django.urls import path
from .views import (
    FreelancerRegisterView,
    FreelancerDetailView,
    UpdateFreelancerSkillsView,
    CreateJobView,
    ListJobsView,
    FilterJobsView,
    ApplyForJobView,
    ViewApplicationsView,
    UpdateApplicationStatusView,
)

urlpatterns = [
    # Freelancer APIs
    path(
        "freelancers/register/",
        FreelancerRegisterView.as_view(),
        name="register_freelancer",
    ),
    path(
        "freelancers/<int:pk>/",
        FreelancerDetailView.as_view(),
        name="freelancer_detail",
    ),
    path(
        "freelancers/<int:pk>/update-skills/",
        UpdateFreelancerSkillsView.as_view(),
        name="update_skills",
    ),
    # Job APIs
    path("jobs/create/", CreateJobView.as_view(), name="create_job"),
    path("jobs/", ListJobsView.as_view(), name="list_jobs"),
    path("jobs/filter/", FilterJobsView.as_view(), name="filter_jobs"),
    # Application APIs
    path("applications/apply/", ApplyForJobView.as_view(), name="apply_job"),
    path(
        "applications/freelancer/<int:freelancer_id>/",
        ViewApplicationsView.as_view(),
        name="view_applications",
    ),
    path(
        "applications/<int:pk>/update-status/",
        UpdateApplicationStatusView.as_view(),
        name="update_application_status",
    ),
]
