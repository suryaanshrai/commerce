# Generated by Django 4.1.5 on 2023-01-19 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_alter_watchlist_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='items',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='items', to='auctions.listing'),
        ),
    ]
