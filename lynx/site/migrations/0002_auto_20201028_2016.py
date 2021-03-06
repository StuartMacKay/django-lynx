# Generated by Django 3.1.2 on 2020-10-28 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("site", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteconfig",
            name="icon",
            field=models.FileField(null=True, upload_to="site"),
        ),
        migrations.AddField(
            model_name="siteconfig",
            name="logo",
            field=models.FileField(null=True, upload_to="site"),
        ),
        migrations.AddField(
            model_name="siteconfig",
            name="title",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="siteconfig",
            name="signups",
            field=models.BooleanField(default=False),
        ),
    ]
