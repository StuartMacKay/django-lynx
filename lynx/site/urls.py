from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/news/')),
    path('account/', include('allauth.urls')),
    path("admin/", admin.site.urls),
    path('news/', include('lynx.news.urls')),
]
