"""network_scanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

# In the urls if the action succeded returns to all automatically
app_name='nmap_scanner'
urlpatterns = [
    path('nmap_scanner_get/', views.ScannerView.as_view(), name='form_scanner_view'),
    path('nmap_scanner_post/', views.ScannerView.as_view(), name='ad_scanner'),
]