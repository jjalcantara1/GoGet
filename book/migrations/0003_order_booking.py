# Generated by Django 4.2.10 on 2024-03-20 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '__first__'),
        ('book', '0002_alter_order_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='booking',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='adminpanel.booking'),
            preserve_default=False,
        ),
    ]
