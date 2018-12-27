from django.urls import path

from . import views


urlpatterns = [
    path('', views.ContentListCreate.as_view(), name="content_list"),
    path('<int:pk>/', views.ContentDetail.as_view(), name="content_detail"),
]
