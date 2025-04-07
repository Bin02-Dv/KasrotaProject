from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dash/', views.dash, name='dash'),
    path('add-violation/', views.add_violation, name='add-violation'),
    path('', views.landing_page, name='landing-page'),
    path('update-status/<int:id>', views.update_status, name='update-status'),
]
