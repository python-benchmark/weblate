# Generated by Django 3.1.4 on 2021-02-17 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("trans", "0120_glossary_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="component",
            name="glossary_name",
        ),
    ]
