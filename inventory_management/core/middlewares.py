from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect

class LoginRequiredMiddleware:
    """
    Middleware to handle authentication for the inventory management system.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print("Auth Middleware is calling...")

        response = self.get_response(request)

        # print("Auth Middleware, returning response...")
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Process the view before it is called.
        """
        # if request.path.startswith('/admin/'):
        #     return None
        if not request.user.is_authenticated:
            if request.resolver_match.url_name in ['employee_login'] or request.path.startswith('/admin/'):
                return None
            return HttpResponse("Unauthorized", status=401)
    

class AuthenticatedUserMiddleware:
    """
    Middleware to ensure that the user is authenticated.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Process the view before it is called.
        """
        # if request.path.startswith('/admin/'):
        #     return None
        if request.user.is_authenticated:
            if request.resolver_match.url_name in ['employee_login']:
                return redirect('core:employee_dashboard')
            return None
        