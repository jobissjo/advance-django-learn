from adrf.serializers import ModelSerializer
from .models import Category, Course, models

import asyncio


class AddUpdateCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CourseListSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    async def ato_representation(self, data):
        if isinstance(data, models.Manager):
            data = data.all()

        tasks = []
        if isinstance(data, models.query.QuerySet):
            tasks = [self.child.ato_representation(item) async for item in data]
        else:
            tasks = [self.child.ato_representation(item) for item in data]
        
        return await asyncio.gather(*tasks)

class CourseAddUpdateSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
