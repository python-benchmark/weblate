# Generated by Django 3.1.1 on 2020-10-29 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0001_squashed_0020_auto_20200320_1007"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="billing",
            name="grace_period",
        ),
    ]
