from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from shorturl.models import ShortUrl

class Index(View):
    def get(self, request):
        return render(request, "index.html")

class Try(View):
    def get(self, request):
        return render(request, "try.html")

    def post(self, request):
        long_url = request.POST.get("long_url", "")
        if not ShortUrl.is_url_valid(long_url):
            messages.warning(request, "Url is not valid")
            return redirect("try")
        
        slug = request.POST.get("slug", "")
        if len(slug) >= settings.GLOBAL_SETTINGS["short_url_slug_length"] and slug:
            messages.warning(request, "Slug is not valid")
            return redirect("try")

        s = ShortUrl(
            long_url=long_url,
            creator=request.user if request.user.is_authenticated else None
        )
        s.slug = slug
        s.save()
        messages.success(request, "Url shorted")
        return render(request, "try.html", {"shorturl": s})
