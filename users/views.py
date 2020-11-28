from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import (LoginView, LogoutView,PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data['username']
        messages.success(request, f'Account was successfully created for {username}!')
        return redirect('login')
    form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


class LogInUser(LoginView):
    template_name = 'users/login.html'


class LogOutUser(LogoutView):
    template_name = 'users/logout.html'


class ResetPassword(PasswordResetView):
    template_name = 'users/password_reset.html'


class ResetPasswordDone(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class ConfirmPasswordReset(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'


class CompletePasswordReset(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

@login_required
def profile(request):
    u_form = UserUpdateForm(request.POST or None, instance=request.user)
    p_form = ProfileUpdateForm(request.POST or None, request.FILES, instance=request.user.profile)

    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, f'Profile updated successfully!')
        return redirect('profile')
        u_form = UserUpdateForm(request.POST or None, instance=request.user)
        p_form = ProfileUpdateForm(request.POST or None, request.FILES, instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)