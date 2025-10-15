from rest_framework import serializers
from .models import FavoriteBreed


class FavoriteBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteBreed
        fields = ['id', 'user', 'breed_id', 'breed_name', 'breed_data', 'last_updated', 'created_at']
        read_only_fields = [' user','id', 'last_updated', 'created_at']