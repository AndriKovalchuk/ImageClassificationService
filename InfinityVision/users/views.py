from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from .forms import RegistrationForm, LoginForm, UserEditForm


class RegisterView(View):
    template_name = "users/register.html"
    form_class = RegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="image_process:my_pdfs")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, context={"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Registration of {username} has been successfully completed.")
            return redirect(to="users:signin")
        return render(request, self.template_name, context={"form": form})


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Registration of {user.username} has been successfully completed.")
            return redirect('users:signin')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'


class UserLogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy("users:logout_page"))


class UserLogoutPageView(TemplateView):
    template_name = 'users/logout.html'


class LoginView(View):
    template_name = "users/login.html"
    form_class = LoginForm

    def get(self, request):
        return render(request, self.template_name, context={"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('image_process:my_images')
            else:
                messages.error(request, 'Invalid username or password.')
        return render(request, self.template_name, context={"form": form})


@login_required
def user_view(request, username):
    user = request.user
    return render(request, 'users/user.html', {'user': user})


@login_required
def edit_user(request, username):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save(commit=False)

            new_password1 = form.cleaned_data.get('new_password1')
            if new_password1:
                user.set_password(new_password1)
                user.save()

                update_session_auth_hash(request, user)
            messages.success(request, "Profile updated successfully.")
            return redirect('users:user_view', username=request.user.username)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'users/edit_user.html', {
        'form': form,
        'username': username
    })


@login_required
def delete_user(request, username):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('users:logout')

    return render(request, 'users/confirm_delete.html')
