# Generated by Django 4.2.4 on 2023-08-14 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("water_reminder_api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="WaterConsumptionDaily",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
    ]
