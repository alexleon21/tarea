from django.shortcuts import redirect

class ValidarURLMiddleware:
    URLS_PERMITIDAS = ['/', '/login', '/registro', '/cuenta'] # Agrega aquí las URLs permitidas en tu aplicación

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path not in self.URLS_PERMITIDAS and not request.user.is_authenticated:
            return redirect('login') # Cambia 'login' por el nombre de la vista o la URL de inicio de sesión de tu aplicación.
        response = self.get_response(request)
        return response