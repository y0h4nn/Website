from .models import Quote


def get_quote(request):
    if request.method in ['POST', 'GET']:
        return {'quote': Quote.get_random()}
