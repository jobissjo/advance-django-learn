from django.http import JsonResponse
from django.views import View
from django.utils.decorators import classonlymethod
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Product

import orjson

@method_decorator(csrf_exempt, name='dispatch')
class ProductView(View):
    
    async def get(self, request, *args, **kwargs):
        products = await Product.all()
        result = [{'id': prod.id, 'name': prod.name, 'price': prod.price} for prod in products]
        return JsonResponse({'data': result}, safe=True)

    async def post(self, request, *args, **kwargs):
        try:
            body_unicode = (await request.body)
            data = orjson.loads(body_unicode.decode('utf-8'))
            name = data.get('name')
            price = data.get('price')

            if not name or not price:
                return JsonResponse({'message': "Price and name are required"}, status=400)

            product = Product(name=name, price=price)
            await product.save()
            return JsonResponse({'message': 'Product created successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    async def put(self, request, *args, **kwargs):
        return JsonResponse({'message': "Not implemented yet"}, status=501)

    async def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': "Not implemented yet"}, status=501)
