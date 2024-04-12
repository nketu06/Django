from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product,Order
from django.db.models import Q,F
from django.db.models.aggregates import Count,Max,Min,Sum,Avg
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from django.core.mail import send_mail,mail_admins,BadHeaderError


def say_hello(request):
    try:
        send_mail('subject','message','nke@gamil.com',['firstreciever@gmail.com','sec@gmail.com'])
    except BadHeaderError:
        pass
    order=TaggedItem.objects.get_tags_for(Product,1)
    # order=Order.objects.aggregate(Count('id'))
    return render(request, 'hello.html', {'name': 'Ketu','products':list(order)})
