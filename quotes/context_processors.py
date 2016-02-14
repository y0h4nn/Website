from .models import Quote


def get_quote(request):
    if request.method in ['POST', 'GET']:
        quote = Quote.get_random()
        if quote:
            return {'quote': quote.text, 'quote_prof': quote.prof}
        else:
            return {'quote': None}
