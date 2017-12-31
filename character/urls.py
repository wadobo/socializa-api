from django.urls import path

from . import views


urlpatterns = [
    path('', views.CharacterListCreate.as_view(), name="character_list"),
    path('<int:pk>/', views.CharacterDetail.as_view(), name="character_detail"),
]
