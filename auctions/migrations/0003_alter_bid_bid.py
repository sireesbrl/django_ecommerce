# Generated by Django 4.2.11 on 2024-06-08 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_remove_bid_bid_listing"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bid",
            name="bid",
            field=models.FloatField(),
        ),
    ]