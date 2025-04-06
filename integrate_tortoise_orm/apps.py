from django.apps import AppConfig
from django.conf import settings
from tortoise import Tortoise
import asyncio


class IntegrateTortoiseOrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'integrate_tortoise_orm'

    def ready(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.init_tortoise())
    
    async def init_tortoise(self):
        await Tortoise.init(config=settings.TORTOISE_ORM)
        await Tortoise.generate_schemas()
