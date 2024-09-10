from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class Food(models.Model):
  Name = models.CharField(max_length=50)
  Category = models.CharField(max_length=50)
  Prize = models.DecimalField(max_digits=5, decimal_places=2)
  Description = models.TextField()
  src = models.CharField(max_length=255)
  star = models.PositiveIntegerField(validators=[MaxValueValidator(5)], default=0)
  def __str__(self):
     return self.Name


class Cart(models.Model):
    product = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    def total(self):
       return f'{self.quantity * self.product.Prize}'
    
  
    def __str__(self):
      return self.user.username
