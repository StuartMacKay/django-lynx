# Generated by Django 3.1.2 on 2020-10-18 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items_per_page', models.IntegerField()),
            ],
            options={
                'verbose_name': 'News Configuration',
                'verbose_name_plural': 'News Configuration',
            },
        ),
    ]
