from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.home, name='home'),
    path('item/delete/<list_id>', views.delete, name='delete'),
    path('item/toggle/<list_id>', views.toggle, name='toggle'),
    path('item/edit/<list_id>', views.edit, name='edit'),
]
