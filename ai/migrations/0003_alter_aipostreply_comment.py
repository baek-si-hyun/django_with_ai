# Generated by Django 5.0.2 on 2024-05-21 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ai", "0002_aiknowhow_aipost"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aipostreply",
            name="comment",
            field=models.CharField(max_length=10000),
        ),
    ]
