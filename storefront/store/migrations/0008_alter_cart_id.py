# Generated by Django 5.0.2 on 2024-02-15 17:02

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0007_rename_reviw_review"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
    ]