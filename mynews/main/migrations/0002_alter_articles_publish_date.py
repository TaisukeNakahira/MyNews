# Generated by Django 4.1 on 2023-07-31 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="articles",
            name="publish_date",
            field=models.DateField(null=True),
        ),
    ]
