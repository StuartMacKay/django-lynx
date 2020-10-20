from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('account/', include('allauth.urls')),
    path("admin/", admin.site.urls),
    path('news/', include('lynx.news.urls')),
]
