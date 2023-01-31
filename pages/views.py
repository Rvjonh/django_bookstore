from django.shortcuts import render

from django.views.generic import TemplateView

from books.models import Book

# Create your views here.


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_5_books = Book.objects.all().order_by("-date_creation")[:5][::-1]
        context["last_5_books"] = last_5_books
        return context


class AboutPageView(TemplateView):
    template_name = "about.html"
