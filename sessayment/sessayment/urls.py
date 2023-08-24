"""sessayment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings
from .views import index, LoginView, RegisterView, logout_view, not_found


urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("logout/", logout_view, name="logout"),
    path("signin/", LoginView.as_view(), name="signin"),
    path("signup/", RegisterView.as_view(), name="register"),
    path("mahasiswa/", include("mahasiswa.urls")),
    path("dosen/", include("dosen.urls")),
    path("admin/", include("custom_admin.urls")),
    path("*", not_found, name="not_found"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
