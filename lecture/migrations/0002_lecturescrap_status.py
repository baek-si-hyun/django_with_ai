# Generated by Django 5.0.2 on 2024-03-06 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturescrap',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
