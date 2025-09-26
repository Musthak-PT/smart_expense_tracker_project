# tracker/models.py
from django.db import models
from django.conf import settings  # for AUTH_USER_MODEL reference

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()
    class Meta:
        ordering = ['-date']
