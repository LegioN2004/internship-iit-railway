from django.urls import path
from pages.views import (root_page_view, dynamic_pages_view, train_report_view)

app_name = "pages"

urlpatterns = [
    path('', root_page_view, name="dashboard"),
    # path('train-report/', train_report_view, name='train_report'),
    path('<str:template_name>/', dynamic_pages_view, name='dynamic_pages')
]