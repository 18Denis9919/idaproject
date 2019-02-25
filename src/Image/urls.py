from django.contrib import admin
from django.urls import path, re_path
from .views import ImageListView, ImageCreateView, ImageDetailView

app_name = 'image'
urlpatterns = [
	path('', ImageListView.as_view(), name = 'list'),
	path('upload/', ImageCreateView.as_view(), name = 'create'),
	path('<slug:slug>/', ImageDetailView.as_view(), name = 'detail'),
]