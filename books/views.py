from django.views.generic import ListView, DetailView, FormView
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db.models import Q

from django.core.paginator import Paginator
from .models import Book, Review

from .forms import ReviewForm, BookForm


class BookListView(ListView):
    paginate_by = 24
    model = Book
    context_object_name = "book_list"
    template_name = "books/book_list.html"
    queryset = Book.objects.all().order_by("-date_creation")


class ReviewGet(DetailView):
    model = Book
    context_object_name = "book"
    template_name = "books/book_detail.html"
    queryset = Book.objects.all().prefetch_related(
        "reviews__author",
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = self.get_review_form()
        context["page_obj"] = self.get_review_pagination(context)
        return context

    def get_review_form(self):
        return ReviewForm()

    def get_review_pagination(self, context):
        """returns pagination for reviews section"""
        reviews_list = Review.objects.filter(book=context["book"])
        paginator = Paginator(reviews_list, 5)
        page = self.request.GET.get("page")
        page_obj = paginator.get_page(page)
        return page_obj


class ReviewPost(SingleObjectMixin, FormView):
    model = Book
    context_object_name = "book"
    form_class = ReviewForm
    template_name = "books/book_detail.html"
    queryset = Book.objects.all().prefetch_related(
        "reviews__author",
    )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        noti_msj = f"{self.request.user} Review was added successfully"
        messages.success(self.request, noti_msj)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        review = form.save(commit=False)
        review.book = self.object
        review.author = self.request.user
        review.save()
        return super().form_valid(form)

    def get_success_url(self):
        book = self.get_object()
        return reverse("book_detail", kwargs={"pk": book.pk})


class BookDetailView(View):
    def get(self, request, *args, **kwargs):
        view = ReviewGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ReviewPost.as_view()
        return view(request, *args, **kwargs)


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


class MyBooksView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Book
    context_object_name = "my_books"
    template_name = "books/book_account.html"

    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(publisher=user)

    def dispatch(self, request, *args, **kwargs):
        """Will send a notification in case user is not logged"""
        if not request.user.is_authenticated:
            messages.error(self.request, "You need to log in")
        return super().dispatch(request, *args, **kwargs)


class NewBookView(LoginRequiredMixin, FormView):
    form_class = BookForm
    template_name = "books/book_new.html"

    def dispatch(self, request, *args, **kwargs):
        """Will send a notification in case user is not logged"""
        if not request.user.is_authenticated:
            messages.error(self.request, "You need to log in to published a book")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        book = form.save(commit=False)
        book.publisher = self.request.user
        book.save()
        self.success_url = reverse("book_detail", kwargs={"pk": book.id})

        if form.is_valid():
            messages.success(self.request, "Book Published Correctly")

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error Publishing Book")
        return super().form_invalid(form)
