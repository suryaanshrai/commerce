# Generated by Django 4.1.5 on 2023-01-19 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_remove_watchlist_items_alter_watchlist_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='items',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='auctions.listing'),
        ),
    ]
