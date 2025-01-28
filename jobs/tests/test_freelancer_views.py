from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from jobs.models import Freelancer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class FreelancerDetailViewTest(APITestCase):

    def setUp(self):
        # Create an admin user and generate a JWT token for authentication
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.admin_token = self.get_jwt_token(self.admin_user)

        # Create a regular user (non-admin)
        self.regular_user = User.objects.create_user(
            username="user", email="user@example.com", password="userpass"
        )
        self.regular_user_token = self.get_jwt_token(self.regular_user)

        # Create a sample freelancer
        self.freelancer = Freelancer.objects.create(
            full_name="John Doe",
            email="johndoe@example.com",
            skills="Python, Django",
        )

        self.detail_url = reverse(
            "freelancer_detail", kwargs={"pk": self.freelancer.id}
        )

    def get_jwt_token(self, user):
        """Generate JWT token for a user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_get_freelancer_detail_valid_admin(self):
        """Test retrieving freelancer details as an admin."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["full_name"], "John Doe")
        self.assertEqual(response.data["email"], "johndoe@example.com")
        self.assertEqual(response.data["skills"], "Python, Django")

    def test_get_freelancer_detail_not_found(self):
        """Test retrieving freelancer details for a non-existent freelancer."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get(reverse("freelancer_detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_freelancer_detail_unauthenticated(self):
        """Test accessing the view without authentication."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_freelancer_detail_non_admin(self):
        """Test accessing the view as a non-admin authenticated user."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.regular_user_token}")
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FreelancerRegisterViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("register_freelancer")

    def test_register_freelancer_valid(self):
        """Test creating a freelancer with valid data"""
        data = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "skills": "Python, Django",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["full_name"], "John Doe")
        self.assertEqual(response.data["email"], "john@example.com")

    def test_register_freelancer_invalid(self):
        """Test creating a freelancer with missing email"""
        data = {"full_name": "Jane Doe", "skills": "Python, Django"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)


class UpdateFreelancerSkillsViewTest(APITestCase):

    def setUp(self):
        # Create users and generate JWT tokens
        self.user = User.objects.create_user(
            username="user1", email="user1@example.com", password="userpass"
        )
        self.token = self.get_jwt_token(self.user)

        # Create a sample freelancer
        self.freelancer = Freelancer.objects.create(
            full_name="Jane Doe",
            email="jane.doe@example.com",
            skills="Python, Django",
        )

        self.update_url = reverse("update_skills", kwargs={"pk": self.freelancer.id})

    def get_jwt_token(self, user):
        """Generate JWT token for a user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_update_freelancer_skills_valid(self):
        """Test successfully updating freelancer skills with valid data."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        data = {"skills": "Python, Django, JavaScript"}
        response = self.client.patch(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["skills"], "Python, Django, JavaScript")

    def test_update_freelancer_skills_invalid_data(self):
        """Test updating freelancer skills with invalid data."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        data = {"skills": ""}  # Invalid as skills should not be empty
        response = self.client.patch(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_freelancer_skills_not_found(self):
        """Test trying to update skills for a non-existent freelancer."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.patch(
            reverse("update_skills", kwargs={"pk": 999}),
            {"skills": "Go"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_freelancer_skills_unauthenticated(self):
        """Test updating freelancer skills without authentication."""
        data = {"skills": "Python, Django, React"}
        response = self.client.patch(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
