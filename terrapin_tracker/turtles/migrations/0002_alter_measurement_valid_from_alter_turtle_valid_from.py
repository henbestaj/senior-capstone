# Generated by Django 4.1.7 on 2023-03-15 16:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("turtles", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="measurement",
            name="valid_from",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 3, 15, 16, 18, 3, 941033, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Valid From",
            ),
        ),
        migrations.AlterField(
            model_name="turtle",
            name="valid_from",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 3, 15, 16, 18, 3, 941033, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Valid From",
            ),
        ),
    ]