# Generated by Django 4.0.4 on 2022-06-02 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postal_code', models.CharField(max_length=8)),
                ('date_exec', models.DateTimeField()),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('data', models.JSONField()),
            ],
        ),
    ]
