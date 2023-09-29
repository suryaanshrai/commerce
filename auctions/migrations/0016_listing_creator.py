# Generated by Django 4.1.5 on 2023-01-17 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_watchlist_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]