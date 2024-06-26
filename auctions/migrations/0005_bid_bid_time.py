# Generated by Django 4.2.11 on 2024-06-08 09:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0004_listings_bid_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="bid",
            name="bid_time",
            field=models.TimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
