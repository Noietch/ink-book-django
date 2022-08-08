# Generated by Django 3.2.8 on 2022-08-08 06:55

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
                ('name', models.CharField(max_length=200)),
                ('encryption', models.CharField(max_length=255, null=True)),
                ('project_id', models.IntegerField(default=0, null=True)),
                ('team_id', models.IntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('avatar', models.TextField(default='https://img.alicdn.com/imgextra/i3/O1CN01fYx7ZL1F2WfrXat17_!!6000000000429-2-tps-600-264.png')),
                ('width', models.IntegerField(default=1440)),
                ('height', models.IntegerField(default=1024)),
                ('label', models.CharField(default='项目计划', max_length=100, null=True)),
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
                ('name', models.CharField(max_length=200)),
                ('team_id', models.IntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('avatar', models.TextField(default='https://dn-st.teambition.net/teambition/images/logo1.a6464e9c.jpg')),
                ('width', models.IntegerField(default=1440)),
                ('height', models.IntegerField(default=1024)),
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
                ('name', models.CharField(max_length=200)),
                ('route', models.CharField(max_length=255, null=True)),
                ('project_id', models.IntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('avatar', models.TextField(default='https://dn-st.teambition.net/teambition/images/logo3.c69aba1a.jpg')),
                ('width', models.IntegerField(default=1440)),
                ('height', models.IntegerField(default=1024)),
                ('components', models.TextField(null=True)),
                ('public', models.BooleanField(default=False)),
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
                ('name', models.CharField(max_length=200)),
                ('route', models.CharField(max_length=255, null=True)),
                ('project_id', models.IntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('avatar', models.TextField(default='https://dn-st.teambition.net/teambition/images/logo5.a07a0ef0.jpg')),
                ('width', models.IntegerField(default=1440)),
                ('height', models.IntegerField(default=1024)),
            ],
            options={
                'verbose_name': 'UML图',
                'verbose_name_plural': 'UML图',
            },
        ),
    ]
