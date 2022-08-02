# Generated by Django 3.2.5 on 2022-08-02 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('route', models.CharField(max_length=255)),
                ('project_id', models.IntegerField()),
            ],
            options={
                'verbose_name': '文档',
                'verbose_name_plural': '文档',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('team_id', models.IntegerField()),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
            },
        ),
        migrations.CreateModel(
            name='Prototype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('route', models.CharField(max_length=255)),
                ('project_id', models.IntegerField()),
            ],
            options={
                'verbose_name': '设计原型',
                'verbose_name_plural': '设计原型',
            },
        ),
        migrations.CreateModel(
            name='UML',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('route', models.CharField(max_length=255)),
                ('project_id', models.IntegerField()),
            ],
            options={
                'verbose_name': 'UML图',
                'verbose_name_plural': 'UML图',
            },
        ),
    ]