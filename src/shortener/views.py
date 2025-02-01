from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .forms import SubmitUrlForm
from .models import KirrURL
from analytics.models import ClickEvent

def test_view(request):
    return HttpResponse("Some Stuff")

def kirr_redirect_view(request, shortcode=None, *args, **kwargs):  # function based view
    #obj = get_object_or_404(KirrURL, shortcode=shortcode)
    obj = KirrURL.objects.get(shortcode=shortcode)
    return HttpResponseRedirect(obj.url)



class URLRedirectView(View):  # class-based view
    def get(self, request, shortcode=None, *args, **kwargs):
        qs = KirrURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404

        obj = qs.first()
        print(ClickEvent.objects.create_event(obj))
        return HttpResponseRedirect(obj.url)

    def post(self, request, *args, **kwargs):
        return HttpResponse()
   
class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()
        context = {
            "title": "Kirr.co",
            "form": the_form
        }
        return render(request, "shortener/home.html", context)

    def post(self, request, *args, **kwargs):
        form = SubmitUrlForm(request.POST)
        context = {
            "title": "Kirr.co",
            "form": form
        }
        template = "shortener/home.html"
        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            obj, created = KirrURL.objects.get_or_create(url=new_url)
            context = {
                "object":obj,
                "created":created,
            }
            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already-exists.html"

        return render(request, template, context)

def home_view_fbv(request,  *args, **kwargs):
    if request.method == "POST":
        print(request.POST)
    return render(request, "shortener/home.html", {})