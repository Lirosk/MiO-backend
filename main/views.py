from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('pashol nahui')

def user(request):
    return HttpResponse('user')

def social(request):
    return HttpResponse('social')