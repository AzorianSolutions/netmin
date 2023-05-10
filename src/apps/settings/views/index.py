import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest

base_uri: str = '/settings'
view_directory: str = 'settings'


@login_required
def index(request: HttpRequest):
    return render(request, os.path.join(view_directory, 'index.jinja2'))
