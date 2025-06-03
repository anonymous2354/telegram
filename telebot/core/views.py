from django.shortcuts import render

# Create your views here.
import os
from django.http import HttpResponse

def show_project_files(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # adjust as needed
    files = os.listdir(base_dir)
    return HttpResponse('<br>'.join(files))