# Generated by Django 5.0.1 on 2024-03-06 19:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auctionedObject', to='auctions.listings')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
