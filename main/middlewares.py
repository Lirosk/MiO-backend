from django.http import HttpRequest, HttpResponse

def my_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        return response
    return middleware