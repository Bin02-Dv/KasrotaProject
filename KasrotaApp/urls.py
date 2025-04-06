from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('dash/', views.dash, name='dash'),
    path('add-violation/', views.add_violation, name='add-violation'),
]
