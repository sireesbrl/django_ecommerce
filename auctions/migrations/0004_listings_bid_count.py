# Generated by Django 4.2.11 on 2024-06-08 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_alter_bid_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="listings",
            name="bid_count",
            field=models.IntegerField(default=0),
        ),
    ]