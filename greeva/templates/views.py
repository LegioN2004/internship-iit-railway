from django.shortcuts import render
from datetime import datetime

# from django.contrib.auth.decorators import login_required
from django.template import TemplateDoesNotExist


# @login_required
def root_page_view(request):
    try:
        return render(request, 'index.html')
    except TemplateDoesNotExist:
        return render(request, 'pages-404.html')


# @login_required
def dynamic_pages_view(request, template_name):
    # Add logic to map template_name to the correct file
    template_map = {
        'index': 'index.html',
        'auth-login': 'pages/auth-login.html',
        'auth-signup': 'pages/auth-signup.html',
        'ground-staff': 'pages/ground-staff/ground-staff.html',
        'train-report': 'pages/ground-staff/train-report.html',
        'station-admin': 'pages/station-admin/index.html',
        'zonal-head': 'pages/zonal-head/zonal-head.html',
        # add more as needed
    }
    template_path = template_map.get(template_name, f'pages/{template_name}.html')
    try:
        return render(request, template_path)
    except TemplateDoesNotExist:
        return render(request, 'pages-404.html')
