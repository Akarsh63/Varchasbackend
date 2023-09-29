from .models import NavBarOptions


def add_variable_to_context(request):
    return {
        'navbaroptions': NavBarOptions.objects.filter(active=True),
    }
