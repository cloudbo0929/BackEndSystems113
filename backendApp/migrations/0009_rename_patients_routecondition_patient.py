# Generated by Django 5.1 on 2024-09-22 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("backendApp", "0008_rename_patient_routecondition_patients"),
    ]

    operations = [
        migrations.RenameField(
            model_name="routecondition",
            old_name="patients",
            new_name="patient",
        ),
    ]
