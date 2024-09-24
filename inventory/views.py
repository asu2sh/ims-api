import logging
from django.core.cache import cache

from .models import Item
from .serializers import ItemSerializer, RegisterSerializer

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


logger = logging.getLogger(__name__)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User registered successfully: {serializer.validated_data['email']}")
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        logger.warning(f"User registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemView(APIView):
    
    def get(self, request, item_id=None):
        if item_id:
            cache_key = f"item_{item_id}"
            item = cache.get(cache_key)
            if item:
                logger.info(f"Item retrieved from cache: {item_id}")
                return Response(item, status=status.HTTP_200_OK)
            try:
                item = Item.objects.get(id=item_id)
                serializer = ItemSerializer(item)
                cache.set(cache_key, serializer.data, timeout=600)
                logger.info(f"Item retrieved from database and cached: {item_id}")
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Item.DoesNotExist:
                logger.error(f"Item not found: {item_id}")
                return Response({"error": "Item not found!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            cache_key = "items_list"
            items = cache.get(cache_key)
            if items:
                logger.info("Items list retrieved from cache.")
                return Response(items, status=status.HTTP_200_OK)
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            cache.set(cache_key, serializer.data, timeout=600)
            logger.info("Items list retrieved from database and cached.")
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete("items_list")
            logger.info(f"Item created successfully: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"Item creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, item_id=None):
        if not item_id:
            logger.warning("Item ID not provided for update.")
            return Response({"error": "Please provide the `item_id` in the URL!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            item = Item.objects.get(id=item_id)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                cache.delete(f"item_{item_id}")
                cache.delete("items_list")
                logger.info(f"Item updated successfully: {item_id}")
                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.warning(f"Item update failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            logger.error(f"Item not found for update: {item_id}")
            return Response({"error": "Item not found!"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, item_id=None):
        if not item_id:
            logger.warning("Item ID not provided for deletion.")
            return Response({"error": "Please provide the `item_id` in the URL!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            item = Item.objects.get(id=item_id)
            item.delete()
            cache.delete(f"item_{item_id}")
            cache.delete("items_list")
            logger.info(f"Item deleted successfully: {item_id}")
            return Response({"message": "Item deleted!"}, status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            logger.error(f"Item not found for deletion: {item_id}")
            return Response({"error": "Item not found!"}, status=status.HTTP_404_NOT_FOUND)
