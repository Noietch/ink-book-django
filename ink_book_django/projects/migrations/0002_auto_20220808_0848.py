# Generated by Django 3.2.8 on 2022-08-08 08:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StarProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('project_id', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': '收藏项目',
                'verbose_name_plural': '收藏项目',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
