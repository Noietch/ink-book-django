# Generated by Django 3.2.8 on 2022-08-07 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prototype',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]