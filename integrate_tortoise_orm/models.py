from tortoise.models import Model
from tortoise import fields

class Product(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=50)
    price = fields.FloatField(default=0)