import csv
from django.core.management.base import BaseCommand
from jobs.models import Freelancer, Job
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = "Import jobs and freelancers from CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file", type=str, help="The path to the CSV file to import data from"
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]

        try:
            with open(csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                freelancers = []
                jobs = []

                for row in reader:
                    # Import Freelancer
                    freelancer_data = {
                        "full_name": row["freelancer_name"],
                        "email": row["freelancer_email"],
                        "skills": row["freelancer_skills"],
                    }
                    freelancer, created = Freelancer.objects.get_or_create(
                        email=row["freelancer_email"], defaults=freelancer_data
                    )
                    if created:
                        freelancers.append(freelancer)

                    # Import Job
                    job_data = {
                        "title": row["job_title"],
                        "description": row["job_description"],
                        "required_skills": row["job_skills"],
                    }
                    job, created = Job.objects.get_or_create(
                        title=row["job_title"], defaults=job_data
                    )
                    if created:
                        jobs.append(job)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully imported {len(freelancers)} freelancers and {len(jobs)} jobs."
                    )
                )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR("The specified CSV file does not exist.")
            )
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(f"Validation error: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
