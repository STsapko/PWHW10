from http.client import HTTPResponse

from django.shortcuts import render, redirect
from django.views import View

from .forms import RegisterForm


class RegisterView(View):
    form_class = RegisterForm
    template_name = "users/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="quotes:root")
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect(to="users:login")
        return render(request, self.template_name, {"form": form})

