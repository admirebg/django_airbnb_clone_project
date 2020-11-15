from django.views import View
from django.views.generic import FormView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from . import forms


# class LoginView(View):
#     def get(self, request):
#         form = forms.LoginForm(initial={"email": "ys@gmail.com"})
#         return render(request, "users/login.html", {"form": form})
#
#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         # print(form)
#
#         print(form.is_valid())  # clean_ 함수들 안에 에러가 발생하지 않으면 is_valid() 값이 True임.
#         if form.is_valid():
#             # print(form.cleaned_data)
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             # authenticate함수를 쓰려면 username 필드를 써야함.
#             user = authenticate(request, username=email, password=password) # cookie 등을 알아서 해줌.
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, "users/login.html", {"form": form})


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        # authenticate함수를 쓰려면 username 필드를 써야함.
        user = authenticate(self.request, username=email, password=password) # cookie 등을 알아서 해줌.
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        'first_name': 'ys',
        'last_name': 'kim',
        'email': 'ys1@gmail.com'
    }

    def form_valid(self, form):
        form.save()     # form 이 valid하면 save 실행. 즉 form이 valid한지 체크한 후에 form_valid함수를 탄다.
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        # authenticate함수를 쓰려면 username 필드를 써야함.
        user = authenticate(self.request, username=email, password=password) # cookie 등을 알아서 해줌.
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
