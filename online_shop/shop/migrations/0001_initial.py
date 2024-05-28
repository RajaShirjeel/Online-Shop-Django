# Generated by Django 5.0.6 on 2024-05-13 15:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('image_url', models.CharField(max_length=400)),
                ('digital', models.BooleanField()),
                ('quantity', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.cart')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.customer')),
                ('products', models.ManyToManyField(to='shop.product')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(through='shop.CartItem', to='shop.product'),
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=300)),
                ('city', models.CharField(max_length=200, null=True)),
                ('state', models.CharField(max_length=200, null=True)),
                ('zipcode', models.CharField(max_length=200, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.customer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_addresses', to='shop.order')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
                ('size', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.size')),
            ],
            options={
                'unique_together': {('product', 'size')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(through='shop.ProductSize', to='shop.size'),
        ),
    ]