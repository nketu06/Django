from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product,Order
from django.db.models import Q,F
from django.db.models.aggregates import Count,Max,Min,Sum,Avg
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem


def say_hello(request):

    order=TaggedItem.objects.get_tags_for(Product,1)
    # order=Order.objects.aggregate(Count('id'))
    return render(request, 'hello.html', {'name': 'Ketu','products':list(order)})
