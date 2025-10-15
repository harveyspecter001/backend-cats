from django.shortcuts import render

# Create your views here.
import requests
import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import FavoriteBreed
from .serializers import FavoriteBreedSerializer

THE_CAT_API_KEY = os.getenv("THE_CAT_API_KEY")
THE_CAT_API_URL = "https://api.thecatapi.com/v1"

class BreedSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '').lower()
        origin = request.query_params.get('origin', '').lower()
        temperament = request.query_params.get('temperament', '').lower()
        headers = {'x-api-key': THE_CAT_API_KEY}
        api_url = f"{THE_CAT_API_URL}/breeds"

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            all_breeds = response.json()

            filtered_breeds = all_breeds

            if query:
                filtered_breeds = [breed for breed in filtered_breeds if query in breed['name'].lower()]
            if origin:
                filtered_breeds = [breed for breed in filtered_breeds if origin in breed['origin'].lower()]
            if temperament:
                filtered_breeds = [breed for breed in filtered_breeds if temperament in breed['temperament'].lower()]

            return Response(filtered_breeds)
        except requests.RequestException as e:
            return Response({"error": "Failed to fetch breeds from The Cat API."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
       
class FavoriteBreedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = FavoriteBreed.objects.filter(user=request.user)
        serializer = FavoriteBreedSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavoriteBreedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class FavoriteBreedDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, breed_id):
        try:
            favorite = FavoriteBreed.objects.get(user=request.user, breed_id=breed_id)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FavoriteBreed.DoesNotExist:
            return Response({"error": "Favorite breed not found."}, status=status.HTTP_404_NOT_FOUND)