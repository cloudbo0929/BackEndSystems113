# Generated by Django 5.1 on 2024-09-17 21:42

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backendApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="line_notify",
            field=models.CharField(blank=True, max_length=45, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="qrcodepoint",
            name="qr_code_image",
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="Bed",
            fields=[
                ("bed_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "bed_number",
                    models.CharField(blank=True, max_length=5, null=True, unique=True),
                ),
                (
                    "created_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="backendApp.patient",
                    ),
                ),
            ],
        ),
    ]
