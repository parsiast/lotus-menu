from django.shortcuts import render, redirect
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
        if request.accepted_renderer.media_type == 'text/html':
            return render(request, 'menu/menu_make.html', {'items': items})
        return Response(serializer.data)

    def post(self, request):
        if request.accepted_renderer.media_type == 'text/html':
            item_name = request.POST.get('item_name')
            price = request.POST.get('price')
            price2 = request.POST.get('price2', 0)  # Default to 0 if not provided

            # Debugging: Print to console to ensure values are captured correctly
            print(f"item_name: {item_name}, price: {price}, price2: {price2}")

            # Check if item_name is being captured
            if not item_name:
                return render(request, 'menu/menu_make.html', {'error': 'Item name is missing'})

            Menu_items.objects.create(item=item_name, price=price, price2=price2)
            return redirect('add_item')
        serializer = MenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class cafemenu_change(APIView):
    def get_object(self, item_name):
        try:
            item = Menu_items.objects.get(item=item_name)
            return item
        except Menu_items.DoesNotExist:
            raise Http404("Item not found")

    def put(self, request, item_name):
        item = self.get_object(item_name)
        serializer = MenueSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_name):
        item = self.get_object(item_name)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





def menu_view(request):
    items = Menu_items.objects.all()
    return render(request, 'menu/menu.html', {'items': items})
