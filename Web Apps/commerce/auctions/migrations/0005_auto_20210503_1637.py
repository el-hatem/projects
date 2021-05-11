# Generated by Django 3.1.8 on 2021-05-03 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auctions', '0004_remove_activelistings_comments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activelistings',
            options={'verbose_name': 'activeListing', 'verbose_name_plural': 'ActiveListings'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='activelistings',
            name='created_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created', to=settings.AUTH_USER_MODEL),
        ),
    ]
