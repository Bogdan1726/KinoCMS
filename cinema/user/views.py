from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView
from django.contrib.auth import logout
from .models import User
from .forms import UserUpdateForm, UserLoginForm, CustomUserCreationForm


# Create your views here.

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'user/pages/login.html'


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user/pages/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно зарегистрированы можете авторизоваться!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):

    login_url = 'login'
    form_class = UserUpdateForm
    model = User
    template_name = 'user/pages/client_page.html'
    success_url = reverse_lazy('user')

    def get_object(self, queryset=None):
        return self.request.user


    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Данные обновлены')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Исправьте ошибки и попробуйте снова')
        return super().form_invalid(form)


def user_logout(request):
    logout(request)
    return redirect('main')
