# Generated by Django 3.2.19 on 2023-06-22 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sample2', '0002_rename_hobby_person_hobbies'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='hobbies',
            new_name='hobby',
        ),
    ]
