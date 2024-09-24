from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item
from .serializers import ItemSerializer


class ItemView(APIView):
    
    def get(self, request, item_id=None):
        if item_id:
            try:
                item = Item.objects.get(id=item_id)
                serializer = ItemSerializer(item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Item.DoesNotExist:
                return Response({"error": "Item not found!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)
    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
            return Response({'message': 'Item deleted!'}, status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            return Response({"error": "Item not found!"}, status=status.HTTP_404_NOT_FOUND)
