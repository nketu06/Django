from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product


def say_hello(request):
    products = Product.objects.filter(unit_price__gt=20)
    return render(request, 'hello.html', {'name': 'Ketu','products':list(products)})
