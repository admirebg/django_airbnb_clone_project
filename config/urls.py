"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static  # static 파일 제공을 돕는 helper
from django.conf import settings  # 파일명이 변경되도 상관없음. 세팅파일을 찾아줌

urlpatterns = [
    path('admin/', admin.site.urls),
    path("rooms/", include("rooms.urls", namespace="rooms")),
    path("uses/", include("users.urls", namespace="users")),
    path("", include("core.urls", namespace="core"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# url: direct request to view
# view: answer request