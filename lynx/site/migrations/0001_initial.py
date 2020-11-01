# Generated by Django 3.1.2 on 2020-10-20 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SiteConfig",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("signups", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Site Configuration",
                "verbose_name_plural": "Site Configuration",
            },
        ),
    ]
