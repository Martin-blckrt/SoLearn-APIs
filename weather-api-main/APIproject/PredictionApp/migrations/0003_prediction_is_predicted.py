# Generated by Django 4.0.4 on 2022-06-08 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PredictionApp', '0002_prediction_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='is_predicted',
            field=models.BooleanField(default=False),
        ),
    ]
