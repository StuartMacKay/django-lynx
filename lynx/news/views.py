from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from lynx.config.models import NewsConfig

from .forms import NewsForm
from .models import News


class NewsList(ListView):
    template_name = "news/news_list.html"
    queryset = News.objects.all()

    def get_paginate_by(self, queryset):
        return NewsConfig.fetch().items_per_page


class NewsAddView(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = "news/news_form.html"
    success_url = reverse_lazy("news-list")

    def form_valid(self, form):
        form.instance.submitted_by_id = self.request.user.pk
        return super().form_valid(form)
