"""reaktor_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from poetry_parser import views

urlpatterns = [
    path('', views.package_list, name='package-list'),
    path('upload/', views.file_upload, name='upload'),
    path('package/<str:package_name>', views.package_page, name='package-page'),
    # Debug views
    path('debug/pacakge-dump', views.dump_packages, name='package-dump'),
    path('debug/installed-packages-dump', views.dump_installed_packages, name='installed-packages-dump'),
    path('debug/reverse-dependencies-dump', views.dump_reverse_dependencies, name='reverse-dependencies-dump'),
    path('debug/clear-session', views.clear_session, name='clear-session'),
]
