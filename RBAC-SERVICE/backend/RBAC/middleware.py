from .models import RequestLog

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            RequestLog.objects.create(
                user=request.user,
                method=request.method,
                endpoint=request.path
            )
        return response