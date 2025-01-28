from django.test import TestCase
from jobs.models import Job, Application, Freelancer


class FreelancerModelTest(TestCase):

    def setUp(self):
        self.freelancer = Freelancer.objects.create(
            full_name="John Doe",
            email="john.doe@example.com",
            skills="Python, Django, JavaScript",
        )

    def test_freelancer_str_method(self):
        expected_str = self.freelancer.full_name
        self.assertEqual(str(self.freelancer), expected_str)


class JobModelTest(TestCase):

    def setUp(self):
        self.job = Job.objects.create(
            title="Python Developer",
            description="We need a Python Developer",
            required_skills="Python, Django",
        )

    def test_job_str_method(self):
        expected_str = self.job.title
        self.assertEqual(str(self.job), expected_str)


class ApplicationModelTest(TestCase):

    def setUp(self):
        self.freelancer = Freelancer.objects.create(
            full_name="John Doe",
            email="john.doe@example.com",
            skills="Python, Django, JavaScript",
        )
        self.job = Job.objects.create(
            title="Python Developer",
            description="We need a Python Developer",
            required_skills="Python, Django",
        )

        self.application = Application.objects.create(
            freelancer=self.freelancer, job=self.job, status="Applied"
        )

    def test_application_str_method(self):
        expected_str = f"{self.freelancer.full_name} applied for {self.job.title}"
        self.assertEqual(str(self.application), expected_str)
