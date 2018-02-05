from django.urls import path

from . import views


urlpatterns = [
    path('', views.GameListCreate.as_view(), name="game_list"),
    path('<int:pk>/', views.GameDetail.as_view(), name="game_detail"),
]
