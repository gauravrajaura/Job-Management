from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Freelancer, Job, Application
from .serializers import (
    FreelancerSerializer,
    JobSerializer,
    ApplicationSerializer,
    UpdateFreelancerSkillsSerializer,
    UpdateApplicationStatusSerializer,
)
from .utils import CustomPagination


# Freelancer APIs
class FreelancerRegisterView(APIView):
    def post(self, request):
        serializer = FreelancerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FreelancerDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        freelancer = get_object_or_404(Freelancer, pk=pk)
        serializer = FreelancerSerializer(freelancer)
        return Response(serializer.data)


class UpdateFreelancerSkillsView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        freelancer = get_object_or_404(Freelancer, pk=pk)
        serializer = UpdateFreelancerSkillsSerializer(
            freelancer, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Job APIs
class CreateJobView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListJobsView(APIView):
    def get(self, request):
        jobs = Job.objects.all().order_by("posted_at")
        paginator = CustomPagination()
        paginated_jobs = paginator.paginate_queryset(jobs, request)
        serializer = JobSerializer(paginated_jobs, many=True)
        return paginator.get_paginated_response(serializer.data)


class FilterJobsView(APIView):
    def get(self, request):
        skills = request.query_params.get("skills", "").split(",")
        jobs = Job.objects.filter(required_skills__icontains=",".join(skills))
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


# Application APIs
class ApplyForJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, freelancer_id):
        applications = Application.objects.filter(freelancer_id=freelancer_id)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class UpdateApplicationStatusView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        serializer = UpdateApplicationStatusSerializer(
            application, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
