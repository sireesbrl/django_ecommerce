# Generated by Django 4.2.11 on 2024-06-07 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bid",
            name="bid_listing",
        ),
    ]
