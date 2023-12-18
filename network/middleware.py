import httpx


class HttpAPIMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        request.my_name = "damir"
        request.api = httpx
        response = self._get_response(request)
        return response

class SecondMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response
