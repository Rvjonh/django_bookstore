from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    SearchResultsListView,
    MyBooksView,
    NewBookView,
)

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("<uuid:pk>", BookDetailView.as_view(), name="book_detail"),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
    path("account/", MyBooksView.as_view(), name="book_account"),
    path("new/", NewBookView.as_view(), name="book_new"),
]
