from django.urls import path
from .views import menu_view, cafemenu_make, cafemenu_change

urlpatterns = [
    path('', menu_view, name='menu'),
    path('add_item/', cafemenu_make.as_view(), name='add_item'),
    path('changeitem/<str:item_name>/', cafemenu_change.as_view(), name='change_item'),
]
