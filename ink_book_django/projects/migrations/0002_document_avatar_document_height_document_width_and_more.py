# Generated by Django 4.0.4 on 2022-08-03 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='document',
        #     name='avatar',
        #     field=models.TextField(default='https://img.alicdn.com/imgextra/i3/O1CN01fYx7ZL1F2WfrXat17_!!6000000000429-2-tps-600-264.png'),
        # ),
        migrations.AddField(
            model_name='document',
            name='height',
            field=models.IntegerField(default=1024),
        ),
        migrations.AddField(
            model_name='document',
            name='width',
            field=models.IntegerField(default=1440),
        ),
        # migrations.AddField(
        #     model_name='project',
        #     name='avatar',
        #     field=models.TextField(default='https://dn-st.teambition.net/teambition/images/logo1.a6464e9c.jpg'),
        # ),
        migrations.AddField(
            model_name='project',
            name='height',
            field=models.IntegerField(default=1024),
        ),
        migrations.AddField(
            model_name='project',
            name='width',
            field=models.IntegerField(default=1440),
        ),
        # migrations.AddField(
        #     model_name='prototype',
        #     name='avatar',
        #     field=models.TextField(default='https://dn-st.teambition.net/teambition/images/logo3.c69aba1a.jpg'),
        # ),
        migrations.AddField(
            model_name='prototype',
            name='height',
            field=models.IntegerField(default=1024),
        ),
        migrations.AddField(
            model_name='prototype',
            name='width',
            field=models.IntegerField(default=1440),
        ),
        # migrations.AddField(
        #     model_name='uml',
        #     name='avatar',
        #     field=models.TextField(default='https://dn-st.teambition.net/teambition/images/logo5.a07a0ef0.jpg'),
        # ),
        migrations.AddField(
            model_name='uml',
            name='height',
            field=models.IntegerField(default=1024),
        ),
        migrations.AddField(
            model_name='uml',
            name='width',
            field=models.IntegerField(default=1440),
        ),
    ]
