from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Book


class BookListView(ListView):
    paginate_by = 24
    model = Book
    context_object_name = "book_list"
    template_name = "books/book_list.html"
    queryset = Book.objects.all().order_by("-date_creation")


class BookDetailView(DetailView):
    model = Book
    context_object_name = "book"
    template_name = "books/book_detail.html"
    queryset = Book.objects.all().prefetch_related(
        "reviews__author",
    )


class SearchResultsListView(ListView):
    paginate_by = 10
    model = Book
    context_object_name = "book_list"
    template_name = "books/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q", None)
        if query:
            return Book.objects.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            ).order_by("-date_creation")
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q")
        return context
