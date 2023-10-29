from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import ShortUrl

# Create your views here.
class Redirect(View):
    def get(self, request, slug):
        shorturl = ShortUrl.objects.filter(slug=slug).first()
        if shorturl is not None:
            url = shorturl.long_url
            shorturl.visits += 1
            shorturl.save()
            return redirect(url)
        return redirect("index")
