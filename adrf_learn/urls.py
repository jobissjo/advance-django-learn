from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'courses', views.CoursesViewSet, basename='async')



urlpatterns = [
    path('category', views.ListCreateCategoryView.as_view(), name='category'),
    path('category/<int:id>', views.RUDCategoryView.as_view(), name='category_rud'),

    path("", include(router.urls)),

    
]