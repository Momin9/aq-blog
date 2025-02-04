from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView, UpdateView, CreateView

from main.models import Blog, BlogComment
from .forms import SignupForm, LoginUserForm, PasswordChangingForm, EditUserProfileForm, UserPublicDetailsForm, \
    BiographyForm
from .models import UserProfile, UserBiography


class signUp(SuccessMessageMixin, generic.CreateView):
    form_class = SignupForm
    template_name = "authors/register.html"
    success_url = reverse_lazy('login')
    success_message = "User has been created, please login with your username and password"

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             "Please enter details properly")
        return redirect('home')


class logIn(generic.View):
    form_class = LoginUserForm
    template_name = "authors/login.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == "POST":
            form = LoginUserForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    messages.success(
                        request, f"You are logged in as {username}")
                    return redirect('home')
                else:
                    messages.error(request, "Error")
            else:
                messages.error(request, "Username or password incorrect")
        form = LoginUserForm()
        return render(request, "authors/login.html", {"form": form})


class logOut(LoginRequiredMixin, generic.View):
    login_url = 'login'

    def get(self, request):
        logout(request)
        messages.success(request, "User logged out")
        return redirect('home')


class profile(LoginRequiredMixin, generic.View):
    model = Blog
    login_url = 'login'
    template_name = "authors/profile.html"

    def get(self, request, user_name):
        user_related_data = Blog.objects.filter(author__username=user_name)[:6]
        user_profile_data = UserProfile.objects.get(user=request.user.id)
        context = {
            "user_related_data": user_related_data,
            'user_profile_data': user_profile_data
        }
        return render(request, self.template_name, context)


class PasswordchangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangingForm
    login_url = 'login'
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, "authors/password_change_success.html")


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    form_class = EditUserProfileForm
    login_url = 'login'
    template_name = "authors/edit_user_profile.html"
    success_url = reverse_lazy('home')
    success_message = "User updated"

    def get_object(slef):
        return slef.request.user

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             "Please submit the form carefully")
        return redirect('home')


class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = User
    login_url = 'login'
    template_name = 'authors/delete_user_confirm.html'
    success_message = "User has been deleted"
    success_url = reverse_lazy('home')


class UpdatePublicDetails(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    login_url = "login"
    form_class = UserPublicDetailsForm
    template_name = "authors/edit_public_details.html"
    success_url = reverse_lazy('home')
    success_message = "User updated"

    def get_object(slef):
        return slef.request.user.user_profile

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Please submit the form carefully")
        return redirect('home')


class Dashboard(LoginRequiredMixin, generic.View):
    login_url = "login"

    def get(self, request):
        user_related_data = Blog.objects.filter(author__username=request.user.username)
        user_comments = BlogComment.objects.filter(author__username=request.user.username)

        paginator = Paginator(user_related_data, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'user_related_data': user_related_data,
            'page_obj': page_obj,
            'user_comments': user_comments
        }
        return render(request, "authors/dashboard.html", context)


class UserBiographyView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = UserBiography
    form_class = BiographyForm
    template_name = "main/create_biography.html"
    success_url = reverse_lazy('biography')
    success_message = "Your biography has been created successfully."

    def form_valid(self, form):
        form.instance.user_profile = self.request.user.user_profile
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser  # Only superusers can create a biography


class UpdateBiographyView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = UserBiography
    form_class = BiographyForm
    template_name = "main/update_biography.html"
    success_url = reverse_lazy('biography')
    success_message = "Your biography has been updated successfully."

    def test_func(self):
        return self.request.user.is_superuser


class SuperuserTemplateMixin:
    def get_template_names(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return ['main/show_biography.html']
        else:
            return ['main/biography.html']


class ShowBiographyView(SuperuserTemplateMixin, ListView):
    model = UserBiography
    context_object_name = 'user_biographies'

    def get_queryset(self):
        self.user = UserProfile.objects.filter(user__is_superuser=True).first()
        return UserBiography.objects.filter(user_profile=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['has_biography'] = self.user.user_biography
        except UserBiography.DoesNotExist:
            context['has_biography'] = None
        return context
