# Generated by Django 4.2.2 on 2024-05-22 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backendApp', '0004_purchasedetail_remove_prescriptiondetails_medicine_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Prescription',
        ),
    ]
