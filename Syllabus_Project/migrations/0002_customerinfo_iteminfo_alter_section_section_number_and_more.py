# Generated by Django 4.2.2 on 2023-10-22 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Syllabus_Project", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomerInfo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("CustomerName", models.CharField(max_length=40)),
                (
                    "CustomerAddress",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "CustomerPhoneNumber",
                    models.CharField(blank=True, max_length=40, null=True),
                ),
                (
                    "CustomerEmail",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ItemInfo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ItemName", models.CharField(max_length=40)),
                (
                    "ItemLocation",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("ItemNumber", models.IntegerField(blank=True)),
                ("ItemPrice", models.IntegerField(blank=True)),
                ("ItemQuantity", models.IntegerField(blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name="section",
            name="section_number",
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name="section",
            unique_together={("section_number", "courses")},
        ),
        migrations.CreateModel(
            name="SalesData",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "Sales_Customer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Syllabus_Project.customerinfo",
                    ),
                ),
            ],
        ),
    ]
