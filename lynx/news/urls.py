from django.urls import path

from .views import NewsAddView
from .views import NewsList

app_name = "news"

urlpatterns = [
    path("", NewsList.as_view(), name="list-items"),
    path("add", NewsAddView.as_view(), name="add-item"),
]
