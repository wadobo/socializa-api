from django.urls import path

from . import views


urlpatterns = [
    path('', views.GameListCreate.as_view(), name="game_list"),
    path('<int:pk>/', views.GameDetail.as_view(), name="game_detail"),
    path('<int:pk>/join/', views.PlayerJoinToGame.as_view(), name="player_join_to_game"),
]
