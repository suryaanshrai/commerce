# Generated by Django 4.1.5 on 2023-01-18 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_listing_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='creator',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
