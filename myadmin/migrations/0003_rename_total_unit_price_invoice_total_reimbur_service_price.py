# Generated by Django 4.2.5 on 2023-10-01 09:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("myadmin", "0002_remove_reimburservice_service_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="invoice",
            old_name="total_unit_price",
            new_name="total_reimbur_service_price",
        ),
    ]
