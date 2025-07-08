from django.shortcuts import render
from datetime import datetime

# from django.contrib.auth.decorators import login_required
from django.template import TemplateDoesNotExist


# @login_required
def root_page_view(request):
    try:
        return render(request, 'pages/index.html')
    except TemplateDoesNotExist:
        return render(request, 'pages/pages-404.html')


def train_report_view(request):
    """Handle train report requests with dynamic data"""
    train_name = request.GET.get('name', 'Unknown Train')
    train_status = request.GET.get('status', 'Unknown')

    # Sample train data - you can replace this with real database queries
    train_data = {
        'train_name': train_name,
        'train_status': train_status,
        'train_number': '49031',
        'train_side': 'Right Side',
        'station_name': 'Katihar Junction',
        'current_time': datetime.now().strftime("%I:%M %p"),
        'current_date': datetime.now().strftime("%d/%m/%Y"),
        'total_doors': 78,
        'otli_si': 0,
        'otli_sm': 0,
        'li_si': 8,
        'li_sm': 1,
        'broken_si': 57,
        'broken_sm': 12,
        # Sample detailed door data
        'door_details': [
            {'position': 1, 'door_number': 1, 'wagon_number': 'WG001', 'marking': 'LI-SI', 'image': ''},
            {'position': 2, 'door_number': 2, 'wagon_number': 'WG001', 'marking': 'LI-SI', 'image': ''},
            {'position': 3, 'door_number': 3, 'wagon_number': 'WG002', 'marking': 'LI-SI', 'image': ''},
            {'position': 4, 'door_number': 4, 'wagon_number': 'WG002', 'marking': 'LI-SI', 'image': ''},
            {'position': 5, 'door_number': 5, 'wagon_number': 'WG003', 'marking': 'LI-SM', 'image': ''},
            {'position': 6, 'door_number': 6, 'wagon_number': 'WG003', 'marking': 'Broken-SM', 'image': ''},
            {'position': 7, 'door_number': 7, 'wagon_number': 'WG004', 'marking': 'Broken-SI', 'image': ''},
            {'position': 8, 'door_number': 8, 'wagon_number': 'WG004', 'marking': 'Broken-SI', 'image': ''},
        ]
    }

    return render(request, 'pages/train-report.html', train_data)


# @login_required
def dynamic_pages_view(request, template_name):
    try:
        return render(request, f'pages/{template_name}.html')
    except TemplateDoesNotExist:
        return render(request, f'pages/pages-404.html')
