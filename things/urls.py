from django.urls import path

from . import views


urlpatterns = [
    path('item/', views.ItemListCreate.as_view(), name="item_list"),
    path('item/<int:pk>/', views.ItemDetail.as_view(), name="item_detail"),
    path('knowledge/', views.KnowledgeListCreate.as_view(), name="knowledge_list"),
    path('knowledge/<int:pk>/', views.KnowledgeDetail.as_view(), name="knowledge_detail"),
    path('rol/', views.RolListCreate.as_view(), name="rol_list"),
    path('rol/<int:pk>/', views.RolDetail.as_view(), name="rol_detail"),
]
