# Generated by Django 2.2 on 2020-09-20 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200919_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='machines',
            name='instance_name',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
