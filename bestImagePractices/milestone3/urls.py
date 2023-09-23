"""milestone3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, re_path
from django.urls import path
from Website.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('contact/', contact_view, name="contacts"),
    path('upload/', file_upload_view, name="File Upload"),
    path('create/', upload_create_view, name="Create Upload"),
    path('login/', login_view, name="login"),
    path('register/', register_view, name="register"),
    re_path(r"^accounts/", include("django.contrib.auth.urls")),
    path('upload/success/', success_view, name="success"),
    path('queue/', queue_view, name="queue"),
    re_path(r"^start_print/(?P<pk>[0-9]+)/$", start_print, name="start_print"),
    re_path(r"^pause_print/(?P<pk>[0-9]+)/$", pause_print, name="pause_print"),
    re_path(r"^delete_file/(?P<pk>[0-9]+)/$", delete_file, name="delete_file"),
    re_path(r"^view_gcode/(?P<pk>[0-9]+)/$", view_gcode, name="view_gcode")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
