# Generated by Django 4.2.3 on 2023-09-06 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("myadmin", "0005_remove_courttype_created_by"),
    ]

    operations = [
        migrations.CreateModel(
            name="Case",
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
                ("case_name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Client",
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
                ("client_name", models.CharField(max_length=255)),
                ("role", models.CharField(max_length=255)),
                ("respondent_name", models.CharField(max_length=255)),
                ("respondent_advocate", models.CharField(max_length=255)),
                (
                    "case",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="myadmin.case"
                    ),
                ),
            ],
        ),
    ]
