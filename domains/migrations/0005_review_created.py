# Generated by Django 3.1 on 2022-01-15 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0004_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='created',
            field=models.DateField(auto_created=True, null=True),
        ),
    ]
