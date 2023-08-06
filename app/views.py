from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet


# Create your views here.
def home (request):
    return HttpResponse('Home page')