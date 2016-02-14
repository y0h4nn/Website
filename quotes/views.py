from django.shortcuts import render, get_object_or_404, redirect
from .forms import QuoteForm, ProfForm
from .models import Quote, Prof


def add_quote(request):
    quote_form = QuoteForm(request.POST or None)
    if quote_form.is_valid():
        quote = quote_form.save(commit=False)
        quote.author = request.user
        quote.save()
        quote_form = QuoteForm()
    context = {'quote_form': quote_form}

    return render(request, 'quotes/add_quote.html', context)


def manage_prof(request):
    prof_form = ProfForm(request.POST or None)
    if prof_form.is_valid():
        prof_form.save()
        prof_form = ProfForm()
    profs = Prof.objects.all()
    context = {'prof_form': prof_form, 'profs': profs}
    return render(request, 'quotes/manage_prof.html', context)


def manage_quotes(request):
    quotes_to_validate = Quote.objects.filter(approved=False)
    quotes = Quote.objects.filter(approved=True)
    context = {'quotes': quotes, 'quotes_to_validate': quotes_to_validate}
    return render(request, 'quotes/manage_quotes.html', context)


def del_prof(request, pid):
    prof = get_object_or_404(Prof, id=pid)
    prof.delete()
    return redirect('quotes:manage_prof')


def del_quote(request, qid):
    quote = get_object_or_404(Quote, id=qid)
    quote.delete()
    return redirect('quotes:manage_quotes')


def approve_quote(request, qid):
    quote = get_object_or_404(Quote, id=qid)
    quote.approved = True
    quote.save()
    return redirect('quotes:manage_quotes')

