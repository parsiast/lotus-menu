from rest_framework.views import APIView
from .models import Menu_items
from .serializers import MenueSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import render


class cafemenu_make(APIView):
    def get(self, request):
        items = Menu_items.objects.all()
        serializer = MenueSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class cafemenu_change(APIView):
    def get_object(self, item_name, new_data=None):
        try:
            # Get the item by name
            item = Menu_items.objects.get(item=item_name)

            if new_data:
                serializer = MenueSerializer(item, data=new_data)
                if not serializer.is_valid():
                    raise ValueError(serializer.errors)

            return item
        except Menu_items.DoesNotExist:
            raise Http404("Item not found")
        except ValueError as e:
            # If there is a validation error, raise an error with the message
            raise Http404(str(e))

    def get(self, request, item_name):
        item = self.get_object(item_name)
        serializer = MenueSerializer(item)
        return Response(serializer.data)

    def put(self, request, item_name):
        item = self.get_object(item_name, new_data=request.data)

        # Update the item if no duplicates were found
        serializer = MenueSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_name):
        item = self.get_object(item_name)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





def menu_view(request):
    items = Menu_items.objects.all()
    return render(request, 'menu/menu.html', {'items': items})
