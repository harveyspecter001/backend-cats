from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FavoriteBreed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    breed_id = models.CharField(max_length=10) # ej: "abys"
    breed_name = models.CharField(max_length=100)
    breed_data = models.JSONField() # Cachear info completa is_available = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
