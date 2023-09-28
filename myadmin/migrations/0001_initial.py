# Generated by Django 4.2.5 on 2023-09-20 04:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ("ref_no", models.CharField(max_length=255, unique=True)),
                ("respondent_name", models.CharField(blank=True, max_length=255)),
                ("respondent_advocate", models.CharField(blank=True, max_length=255)),
                (
                    "case_type",
                    models.CharField(
                        choices=[
                            ("MISC", "MISC"),
                            ("CRI", "CRI"),
                            ("LIT", "LIT"),
                            ("CONV", "CONV"),
                        ],
                        max_length=255,
                    ),
                ),
                ("case_description", models.TextField(blank=True)),
                ("sense_of_urgent", models.CharField(max_length=20)),
                ("court_no", models.CharField(blank=True, max_length=40)),
                ("judge_name", models.CharField(blank=True, max_length=100)),
                ("court_remark", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="ClientRole",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("client_role", models.CharField(max_length=100)),
                (
                    "client_role_description",
                    models.CharField(blank=True, max_length=500),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CourtType",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("court_type", models.CharField(max_length=100)),
                ("court_description", models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name="Invoice",
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
                ("invoice_date_time", models.DateTimeField(auto_now_add=True)),
                ("final_total", models.DecimalField(decimal_places=2, max_digits=10)),
                ("paid", models.BooleanField(default=False)),
                ("short_descriptions", models.TextField(blank=True, max_length=100)),
                (
                    "total_unit_price",
                    models.DecimalField(decimal_places=2, max_digits=100),
                ),
                (
                    "total_prof_service_price",
                    models.DecimalField(decimal_places=2, max_digits=100),
                ),
                (
                    "case",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="myadmin.case"
                    ),
                ),
            ],
            options={
                "verbose_name": "Invoice",
                "verbose_name_plural": "Invoices",
            },
        ),
        migrations.CreateModel(
            name="ReimburService",
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
                ("service", models.CharField(max_length=100)),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=1000)),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="myadmin.invoice",
                    ),
                ),
            ],
            options={
                "verbose_name": "ReimburService",
                "verbose_name_plural": "ReimburService",
            },
        ),
        migrations.CreateModel(
            name="ProfService",
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
                ("prof_service", models.CharField(max_length=100)),
                (
                    "prof_service_price",
                    models.DecimalField(decimal_places=2, max_digits=1000),
                ),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="myadmin.invoice",
                    ),
                ),
            ],
            options={
                "verbose_name": "ProfService",
                "verbose_name_plural": "ProfService",
            },
        ),
        migrations.CreateModel(
            name="ClientRecord",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("full_name", models.CharField(max_length=100)),
                ("identity", models.CharField(max_length=50, unique=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("other", "Other"),
                        ],
                        max_length=10,
                    ),
                ),
                ("phone_number", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                ("address1", models.CharField(max_length=200)),
                ("address2", models.CharField(blank=True, max_length=200)),
                ("city", models.CharField(max_length=100)),
                ("postcode", models.CharField(max_length=20)),
                ("state", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=100)),
                ("remark", models.CharField(blank=True, max_length=500)),
                ("agent_fullname", models.CharField(blank=True, max_length=100)),
                ("agent_ph", models.CharField(blank=True, max_length=50)),
                ("agent_identity", models.CharField(blank=True, max_length=50)),
                ("latitude", models.FloatField(blank=True)),
                ("longitude", models.FloatField(blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="case",
            name="client_role",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="myadmin.clientrole"
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="clients",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="myadmin.clientrecord"
            ),
        ),
        migrations.AddField(
            model_name="case",
            name="court_type",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="myadmin.courttype",
            ),
        ),
    ]
