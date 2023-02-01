from django import forms

from .models import Review, Book


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("review",)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            "title",
            "author",
            "price",
            "cover",
        )
