# Generated by Django 5.0.6 on 2024-06-28 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagetotextapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='url',
            field=models.CharField(max_length=2048),
        ),
    ]
