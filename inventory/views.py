from django.core.cache import cache

from .models import Item
from .serializers import ItemSerializer, RegisterSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemView(APIView):
    
    def get(self, request, item_id=None):
        if item_id:
            cache_key = f"item_{item_id}"
            item = cache.get(cache_key)
            if item:
                return Response(item, status=status.HTTP_200_OK)
            try:
                item = Item.objects.get(id=item_id)
                serializer = ItemSerializer(item)
                cache.set(cache_key, serializer.data, timeout=600)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Item.DoesNotExist:
                return Response({"error": "Item not found!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            cache_key = "items_list"
            items = cache.get(cache_key)
            if items:
                return Response(items, status=status.HTTP_200_OK)
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            cache.set(cache_key, serializer.data, timeout=600)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete("items_list")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, item_id=None):
        if not item_id:
            return Response({"error": "Please provide the `item_id` in the URL!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            item = Item.objects.get(id=item_id)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                cache.delete(f"item_{item_id}")
                cache.delete("items_list")
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            return Response({"error": "Item not found!"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, item_id=None):
        if not item_id:
            return Response({"error": "Please provide the `item_id` in the URL!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            item = Item.objects.get(id=item_id)
            item.delete()
            cache.delete(f"item_{item_id}")
            cache.delete("items_list")
            return Response({"message": "Item deleted!"}, status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            return Response({"error": "Item not found!"}, status=status.HTTP_404_NOT_FOUND)
