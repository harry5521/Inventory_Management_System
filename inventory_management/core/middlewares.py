from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect

class LoginRequiredMiddleware:
    """
    Middleware to handle that non-authenticated users cannot access dashboards and certain views.
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
    

class LoginPageRestrictionMiddleware:
    """
    Middleware to ensure that authenticated users cannot access the login page.
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
                # Check user's group or role
                if request.user.groups.filter(name='Manager').exists():
                    return redirect('core:manager_dashboard')
                elif request.user.groups.filter(name='Employee').exists():
                    return redirect('core:employee_dashboard')
                elif request.user.groups.filter(name='Moderator').exists():
                    return redirect('core:moderator_dashboard')
                elif request.user.is_superuser:
                    return redirect('/admin/')
                # Fallback if no group matched
                return HttpResponseServerError("You are doing something wrong.")
        return None
        

class GroupNameBasedURLRestrictionMiddleware:
    """
    Middleware to ensure that users can only access views within their assigned roles and namespaces.
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

        user_map = {
            'Manager': '/manager-dashboard/',
            'Employee': '/employee-dashboard/',
            'Moderator': '/moderator-dashboard/',
        }

        if request.user.is_authenticated:
            user_groups = [group.name for group in request.user.groups.all()]
            url_path = request.path

            for group, allowed_url in user_map.items():
                if url_path.startswith(allowed_url):
                    if group in user_groups:
                        return None
                    else:
                        return HttpResponseServerError(f"Access denied. Your Group {user_groups} have No permission to access '{url_path}' URL")

        return None
