from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserUpdateProfileForm

# Create your views here.


class UpdateProfileView(LoginRequiredMixin, FormView):
    template_name = "account/update_profile.html"
    form_class = CustomUserUpdateProfileForm
    success_url = reverse_lazy("account_profile")

    def dispatch(self, request, *args, **kwargs):
        """Will send a notification in case user is not logged"""
        if not request.user.is_authenticated:
            messages.error(self.request, "You need to log in to check your profile")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(UpdateProfileView, self).get_initial()
        if self.request.user.is_authenticated:
            initial.update({"username": self.request.user})
        return initial

    def form_valid(self, form):
        new_username = form.cleaned_data.get("username", None)
        if new_username is not None:
            actual_user = get_user_model().objects.get(username=self.request.user)
            actual_user.username = new_username
            actual_user.save()
            messages.success(self.request, "Profile Updated!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Action denied!")
        return super().form_invalid(form)
