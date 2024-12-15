from rest_framework import serializers
from .models import Menu_items

class MenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu_items
        fields = '__all__'
