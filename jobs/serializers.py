from rest_framework import serializers
from .models import Freelancer, Job, Application


class FreelancerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = ["id", "full_name", "email", "skills", "created_at"]


class UpdateFreelancerSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = ["skills"]


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["id", "title", "description", "required_skills", "posted_at"]


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "freelancer", "job", "status", "applied_at"]


class UpdateApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["status"]
