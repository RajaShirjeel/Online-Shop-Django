# Generated by Django 5.0.6 on 2024-05-21 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_cartitem_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.AddField(
            model_name='order',
            name='cart_items',
            field=models.ManyToManyField(to='shop.cartitem'),
        ),
    ]