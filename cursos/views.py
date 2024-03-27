from django.shortcuts import render
from django.http import HttpResponse

import datetime


# Create your views here.
def home(request):
    now = datetime.datetime.now()
    return HttpResponse(
        f"Bienvenido a primera página web. La hora del servidor es {now.strftime('%A, %d %B, %Y a las %X')}."
    )
