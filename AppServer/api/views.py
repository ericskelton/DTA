from django.shortcuts import render
from rest_framework import viewsets
from .serializers import DetectiveSerializer
from .models import Detectives

class DetectoveViewSet(viewsets.ModelViewSet):
    queryset = Detectives.objects.all().order_by('name')
    serializer_class = DetectiveSerializer