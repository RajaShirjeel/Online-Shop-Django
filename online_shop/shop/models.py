from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg

# Create your models here.

class Size(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image_url = models.CharField(max_length=400)
    digital = models.BooleanField(blank=False)
    sizes =  models.ManyToManyField(Size, through='ProductSize')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.name
    
    @property
    def get_average_rating(self):
        return round(
            self.comment_set.aggregate(Avg('rating'))['rating__avg'] or 0, 1
        )


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)
    available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('product', 'size')

    def __str__(self):
        return f"{self.size.name} - {self.product.name}"

    def get_available_sizes(self):
        return self.sizes.filter(available=True)


class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart ID: {self.id} - Customer: {self.customer.username}"
    
    @property
    def get_total(self):
        total = 0
        cart_items = CartItem.objects.filter(cart=self)
        for item in cart_items:
            total += item.product.price * item.quantity

        return total


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.cart.customer.username}"
    
    @property
    def get_total_product(self):
        total = 0
        total += self.product.price * self.quantity  
        return total
    


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order Id: {self.id} - Customer: {self.customer.username}'
    
    @property
    def get_total(self):
        total = 0
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.product.price * item.quantity
        
        return total
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=200, null=True)

    @property
    def get_total_product(self):
        total = 0
        total += self.quantity * self.product.price
        return total
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, related_name='shipping_addresses')
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Customer: {self.customer.username} - Id: {self.id}'


