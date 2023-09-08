import json
from collections import Counter

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import AddAuthorForm, AddQuoteForm
from .models import Quotes, Author


def main(request):
    quotes = Quotes.objects.all().order_by("-created_at")

    return render(request, "quotes/index.html",
                  context={"quotes": quotes})


def author_info(request, a_fullname):
    author_inf = Author.objects.get(fullname=a_fullname)
    quotes_by_author = Quotes.objects.filter(author__fullname=a_fullname)
    return render(request, "quotes/author_quotes.html", context={"quotes": quotes_by_author, "author_info": author_inf})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = AddAuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})


@login_required
def add_quote(request):
    authors = Author.objects.all()

    if request.method == 'POST':
        form = AddQuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = AddQuoteForm()

    context = {'form': form, "author": authors}
    return render(request, 'quotes/add_quote.html', context)
