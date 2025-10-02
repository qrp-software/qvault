from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

class HomePage(TemplateView):
    template_name = "home.html"


class WelcomePage(TemplateView):
    template_name = "welcome.html"


class ThanksPage(TemplateView):
    template_name = "thanks.html"


class RobotsView(TemplateView):
    template_name = "robots.txt"
    content_type = "text/plain"