from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from jobs.models import Job, Freelancer, Application
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class ApplyForJobViewTest(APITestCase):

    def setUp(self):
        self.freelancer_user = User.objects.create_user(
            username="freelancer",
            email="freelancer@example.com",
            password="freelancerpass",
        )
        self.freelancer_token = self.get_jwt_token(self.freelancer_user)

        self.freelancer = Freelancer.objects.create(
            full_name="John Doe",
            email="freelancer@example.com",
            skills="Python, Django",
        )

        self.job = Job.objects.create(
            title="Backend Developer",
            description="We need a backend developer with experience in Django.",
            required_skills="Python, Django, REST API",
        )

        self.apply_job_url = reverse("apply_job")

    def get_jwt_token(self, user):
        """Generate JWT token for a user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_apply_for_job_valid(self):
        """Test applying for a job with valid data."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.freelancer_token}")
        data = {
            "freelancer": self.freelancer.id,
            "job": self.job.id,
            "status": "Applied",
        }
        response = self.client.post(self.apply_job_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(response.data["freelancer"], self.freelancer.id)
        self.assertEqual(response.data["job"], self.job.id)

    def test_apply_for_job_invalid_data(self):
        """Test applying for a job with invalid data."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.freelancer_token}")
        data = {
            "freelancer": self.freelancer.id,  # Missing job field
        }
        response = self.client.post(self.apply_job_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("job", response.data)  # Check for job field error

    def test_apply_for_job_unauthenticated(self):
        """Test applying for a job without authentication."""
        data = {
            "freelancer": self.freelancer.id,
            "job": self.job.id,
            "status": "Applied",
        }
        response = self.client.post(self.apply_job_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_apply_for_job_invalid_freelancer(self):
        """Test applying for a job with an invalid freelancer ID."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.freelancer_token}")
        data = {
            "freelancer": 9999,  # Non-existent freelancer ID
            "job": self.job.id,
            "status": "Applied",
        }
        response = self.client.post(self.apply_job_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("freelancer", response.data)  # Check for freelancer field error


class ViewApplicationsViewTest(APITestCase):

    def setUp(self):
        self.freelancer_user = User.objects.create_user(
            username="freelancer",
            email="freelancer@example.com",
            password="freelancerpass",
        )
        self.freelancer_token = self.get_jwt_token(self.freelancer_user)

        self.freelancer = Freelancer.objects.create(
            full_name="John Doe",
            email="freelancer@example.com",
            skills="Python, Django",
        )

        self.other_freelancer = Freelancer.objects.create(
            full_name="Jane Smith",
            email="jane.smith@example.com",
            skills="JavaScript, React",
        )

        self.job1 = Job.objects.create(
            title="Backend Developer",
            description="We need a backend developer with experience in Django.",
            required_skills="Python, Django",
        )
        self.job2 = Job.objects.create(
            title="Frontend Developer",
            description="We need a frontend developer with experience in React.",
            required_skills="JavaScript, React",
        )

        self.application1 = Application.objects.create(
            freelancer=self.freelancer, job=self.job1, status="Applied"
        )
        self.application2 = Application.objects.create(
            freelancer=self.freelancer, job=self.job2, status="Shortlisted"
        )

        self.view_applications_url = reverse(
            "view_applications", args=[self.freelancer.id]
        )

    def get_jwt_token(self, user):
        """Generate JWT token for a user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_view_applications_valid_freelancer(self):
        """Test viewing applications for a valid freelancer."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.freelancer_token}")
        response = self.client.get(self.view_applications_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two applications
        self.assertEqual(response.data[0]["freelancer"], self.freelancer.id)

    def test_view_applications_no_applications(self):
        """Test viewing applications for a freelancer with no applications."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.freelancer_token}")
        url = reverse("view_applications", args=[self.other_freelancer.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No applications

    def test_view_applications_unauthenticated(self):
        """Test viewing applications without authentication."""
        response = self.client.get(self.view_applications_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_view_applications_invalid_freelancer(self):
        """Test viewing applications for a non-existent freelancer."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.freelancer_token}")
        url = reverse("view_applications", args=[9999])  # Non-existent freelancer ID
        response = self.client.get(url, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Empty list returned
        self.assertEqual(len(response.data), 0)


class UpdateApplicationStatusViewTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.admin_token = self.get_jwt_token(self.admin_user)

        self.freelancer = Freelancer.objects.create(
            full_name="John Doe",
            email="freelancer@example.com",
            skills="Python, Django",
        )

        self.job = Job.objects.create(
            title="Backend Developer",
            description="We need a backend developer with experience in Django.",
            required_skills="Python, Django",
        )

        self.application = Application.objects.create(
            freelancer=self.freelancer, job=self.job, status="Applied"
        )

        self.update_application_status_url = reverse(
            "update_application_status", args=[self.application.id]
        )

    def get_jwt_token(self, user):
        """Generate JWT token for a user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_update_application_status_valid(self):
        """Test updating the status of an application with valid data."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        payload = {"status": "Shortlisted"}
        response = self.client.patch(
            self.update_application_status_url, data=payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Shortlisted")

    def test_update_application_status_invalid_status(self):
        """Test updating the status with an invalid status value."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        payload = {"status": "InvalidStatus"}
        response = self.client.patch(
            self.update_application_status_url, data=payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", response.data)

    def test_update_application_status_unauthenticated(self):
        """Test updating the status without authentication."""
        payload = {"status": "Shortlisted"}
        response = self.client.patch(
            self.update_application_status_url, data=payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_application_status_non_admin(self):
        """Test updating the status with a non-admin user."""
        non_admin_user = User.objects.create_user(
            username="user", email="user@example.com", password="userpass"
        )
        non_admin_token = self.get_jwt_token(non_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {non_admin_token}")
        payload = {"status": "Shortlisted"}
        response = self.client.patch(
            self.update_application_status_url, data=payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_application_status_non_existent_application(self):
        """Test updating the status of a non-existent application."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        url = reverse(
            "update_application_status", args=[9999]
        )  # Non-existent application ID
        payload = {"status": "Shortlisted"}
        response = self.client.patch(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
