from adrf.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Category, Course
from .serializers import CategoryListSerializer, AddUpdateCategorySerializer, CourseAddUpdateSerializer, CourseListSerializer
from django.core.cache import cache
from rest_framework.response import Response
import orjson
from adrf.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema
from asgiref.sync import sync_to_async
from django.db.models import QuerySet


class ListCreateCategoryView(ListCreateAPIView):
    queryset = Category.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddUpdateCategorySerializer
        return CategoryListSerializer
    
    async def create(self, request, *args, **kwargs):
        return await super().create(request, *args, **kwargs)
    
    async def list(self, request, *args, **kwargs):
        cache_key = "category_list"
        cached_data = await cache.get(cache_key)
        
        if cached_data:
            return Response(orjson.loads(cached_data)) 
        
        response = await super().list(request, *args, **kwargs)
        await cache.set(cache_key, orjson.dumps(response.data), timeout=60)
        
        return response


class RUDCategoryView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return AddUpdateCategorySerializer
        return self.serializer_class

    async def retrieve(self, request, *args, **kwargs):

        return await super().retrieve(request, *args, **kwargs)
    
    async def update(self, request, *args, **kwargs):
        return await super().update(request, *args, **kwargs)
    
    async def destroy(self, request, *args, **kwargs):
        return await super().destroy(request, *args, **kwargs)
    
@extend_schema(tags=['Course'])
class CoursesViewSet(ModelViewSet):
    lookup_field = 'id'

    async def get_queryset(self) -> QuerySet:
        return await sync_to_async(list)(Course.objects.all())

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return CourseAddUpdateSerializer
        return CourseListSerializer
    
    async def list(self, request, *args, **kwargs):
        queryset = await self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    async def retrieve(self, request, *args, **kwargs):
        try:
            course_id = kwargs['id']
            course = await Course.objects.aget(id=course_id)
            return Response(CourseListSerializer(course).data)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"},status=404)
    
    async def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if not await sync_to_async(serializer.is_valid)():
            return Response(serializer.errors, status=400)
        validated_data = serializer.validated_data
        await Course.objects.acreate(**validated_data)
        
        return Response(serializer.data)
    
    async def update(self, request, *args, **kwargs):
        course_id = kwargs['id']
        course = await Course.objects.aget(id=course_id)
        
        serializer = self.get_serializer(course, data=request.data)
        if not await sync_to_async(serializer.is_valid)():
            return Response(serializer.errors, status=400)
        validated_data = serializer.validated_data
        for key, val in validated_data.items():
            setattr(course, key, val)
        await sync_to_async(course.save)()

        return Response(serializer.data)
    
    async def partial_update(self, request, *args, **kwargs):
        course_id = kwargs['id']
        course = await Course.objects.aget(id=course_id)
        
        serializer = self.get_serializer(course, data=request.data, partial=True)
        if not await sync_to_async(serializer.is_valid)():
            return Response(serializer.errors, status=400)
        validated_data = serializer.validated_data
        for key, val in validated_data.items():
            setattr(course, key, val)
        await sync_to_async(course.save)()
        return Response(serializer.data)
    
    async def destroy(self, request, *args, **kwargs):
        course_id = kwargs['id']
        course = await Course.objects.aget(id=course_id)
        await course.adelete()
        return Response({"message": "Course deleted successfully"}, status=200)