# Generated by Django 3.2.8 on 2022-08-09 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_prototype_encryption'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='content',
            field=models.TextField(null=True),
        ),
    ]
