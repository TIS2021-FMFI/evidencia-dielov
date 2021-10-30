from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. Here will we something for post get and so on")