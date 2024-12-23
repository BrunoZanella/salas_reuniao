from django.shortcuts import redirect

class SessionExpireRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if request.path != '/':
                return redirect('/')
        return self.get_response(request)
