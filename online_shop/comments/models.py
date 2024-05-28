from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='images/comment_images', null=True, blank=True)
    created_on = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f'Comment by {self.user} on {self.product}'
    
    @property
    def get_rating(self):
        return range(self.rating)