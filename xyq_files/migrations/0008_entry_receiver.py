# Generated by Django 4.2.18 on 2025-04-04 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('xyq_files', '0007_reply_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_entries', to=settings.AUTH_USER_MODEL),
        ),
    ]
