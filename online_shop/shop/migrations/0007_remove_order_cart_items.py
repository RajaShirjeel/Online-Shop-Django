# Generated by Django 5.0.6 on 2024-05-23 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart_items',
        ),
    ]