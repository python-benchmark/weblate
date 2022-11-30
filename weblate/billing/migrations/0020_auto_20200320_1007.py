# Generated by Django 3.0.4 on 2020-03-20 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0019_slugify"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="slug",
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
