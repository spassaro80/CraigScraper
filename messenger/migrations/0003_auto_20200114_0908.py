# Generated by Django 2.0.2 on 2020-01-14 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0002_auto_20200114_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
