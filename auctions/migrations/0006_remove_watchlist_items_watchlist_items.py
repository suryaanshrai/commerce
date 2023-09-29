# Generated by Django 4.1.5 on 2023-01-16 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='items',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='items',
            field=models.ManyToManyField(blank=True, to='auctions.listing'),
        ),
    ]
