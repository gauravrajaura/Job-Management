from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from jobs.models import Job, Freelancer, Application
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class CreateJobViewTest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.admin_token = self.get_jwt_token(self.admin_user)

        self.regular_user = User.objects.create_user(
            username="user", email="user@example.com", password="userpass"
        )
        self.regular_user_token = self.get_jwt_token(self.regular_user)

        self.create_job_url = reverse("create_job")

    def get_jwt_token(self, user):
        """Generate JWT token for a user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_job_valid(self):
        """Test creating a job with valid data as an admin user."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        data = {
            "title": "Backend Developer",
            "description": "We need a backend developer with experience in Django.",
            "required_skills": "Python, Django, REST API",
        }
        response = self.client.post(self.create_job_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 1)
        self.assertEqual(response.data["title"], "Backend Developer")

    def test_create_job_invalid_data(self):
        """Test creating a job with invalid data."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        data = {
            "title": "",  # Invalid: title is empty
            "description": "We need a backend developer with experience in Django.",
            "required_skills": "Python, Django, REST API",
        }
        response = self.client.post(self.create_job_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)  # Check for error in the title field

    def test_create_job_unauthorized(self):
        """Test creating a job as a regular (non-admin) user."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.regular_user_token}")
        data = {
            "title": "Frontend Developer",
            "description": "We need a frontend developer with React experience.",
            "required_skills": "JavaScript, React, CSS",
        }
        response = self.client.post(self.create_job_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_job_unauthenticated(self):
        """Test creating a job without authentication."""
        data = {
            "title": "Full-Stack Developer",
            "description": "Looking for a versatile full-stack developer.",
            "required_skills": "Python, Django, React",
        }
        response = self.client.post(self.create_job_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ListJobsViewTest(APITestCase):

    def setUp(self):
        # Create multiple Job instances
        Job.objects.create(
            title="Python Developer",
            description="Looking for a Python developer",
            required_skills="Python, Django",
        )
        Job.objects.create(
            title="JavaScript Developer",
            description="Looking for a JavaScript developer",
            required_skills="JavaScript, React",
        )
        Job.objects.create(
            title="Full Stack Developer",
            description="Looking for a Full Stack developer",
            required_skills="Python, JavaScript, Django",
        )

    def test_list_jobs_pagination(self):
        url = reverse("list_jobs")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_jobs_no_pagination(self):
        url = reverse("list_jobs")
        response = self.client.get(url + "?page=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FilterJobsViewTest(APITestCase):

    def setUp(self):
        # Create Job instances with different required skills
        Job.objects.create(
            title="Python Developer",
            description="Looking for a Python developer",
            required_skills="Python, Django",
        )
        Job.objects.create(
            title="JavaScript Developer",
            description="Looking for a JavaScript developer",
            required_skills="JavaScript, React",
        )
        Job.objects.create(
            title="Full Stack Developer",
            description="Looking for a Full Stack developer",
            required_skills="Python, JavaScript, Django",
        )

    def test_filter_jobs_by_skills(self):
        url = reverse("filter_jobs")
        response = self.client.get(url, {"skills": "Python"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 2
        )  # Two jobs should have Python as a required skill

        # Test filtering by a non-existent skill (Ruby)
        response = self.client.get(url, {"skills": "Ruby"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 0
        )  # No jobs should have Ruby as a required skill
