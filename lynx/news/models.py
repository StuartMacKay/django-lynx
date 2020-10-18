from urllib.parse import urlparse

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _


class NewsQuerySet(QuerySet):
    pass


class News(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.TextField()
    url = models.URLField()

    title.verbose_name = _("Title")
    url.verbose_name = _("URL")

    objects = NewsQuerySet.as_manager()

    class Meta:
        verbose_name_plural = _("News")
        ordering = ("-created",)
        get_latest_by = "-created"

    def domain(self):
        return urlparse(self.url).netloc if self.url else None

    def submitter(self):
        return self.submitted_by.username
