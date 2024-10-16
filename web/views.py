from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from .models import TextBlock, Game, Faq, Image, FeaturesText

from users.forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm

def index(request):
    # Text
    header_text_home = get_object_or_404(TextBlock, identifier='header_text_home')
    header_text_catalog = get_object_or_404(TextBlock, identifier='header_text_catalog')
    header_text_contact = get_object_or_404(TextBlock, identifier='header_text_contact')
    header_text_features = get_object_or_404(TextBlock, identifier='header_text_features')
    home_title = get_object_or_404(TextBlock, identifier='home_title')
    home_text = get_object_or_404(TextBlock, identifier='home_text')
    home_tex2 = get_object_or_404(TextBlock, identifier='home_text2')
    button_text1 = get_object_or_404(TextBlock, identifier='button_text1')
    button_text2 = get_object_or_404(TextBlock, identifier='button_text2')
    button_text3 = get_object_or_404(TextBlock, identifier='button_text3')
    title_features = get_object_or_404(TextBlock, identifier='title_features')
    jane = get_object_or_404(TextBlock, identifier='jane')
    des = get_object_or_404(TextBlock, identifier='des')
    view = get_object_or_404(TextBlock, identifier='view')
    discount = get_object_or_404(TextBlock, identifier='discount')
    contact = get_object_or_404(TextBlock, identifier='contact')
    # Text

    # Images
    background = get_object_or_404(Image, identifier='background')
    man_with_items = get_object_or_404(Image, identifier='man_with_items')
    man = get_object_or_404(Image, identifier='man')
    vh = get_object_or_404(Image, identifier='vh')
    users = get_object_or_404(Image, identifier='users')
    logo = get_object_or_404(Image, identifier='logo')
    woman_with_comment = get_object_or_404(Image, identifier='woman_with_comment')
    comment = get_object_or_404(Image, identifier='comment')
    woman = get_object_or_404(Image, identifier='woman')
    # Images
    features = FeaturesText.objects.all()
    games = Game.objects.all()
    faqs = Faq.objects.all()

    return render(request, 'web/index.html', {
        # Text
        'header_text_home': header_text_home,
        'header_text_catalog': header_text_catalog,
        'header_text_contact': header_text_contact,
        'header_text_features': header_text_features,
        'home_title': home_title,
        'home_text': home_text,
        'home_tex2': home_tex2,
        'button_text1': button_text1,
        'button_text2': button_text2,
        'button_text3': button_text3,
        'title_features': title_features,
        'jane': jane,
        'des': des,
        'view': view,
        'discount': discount,
        'contact': contact,
        # Text

        # Images
        'background': background,
        'man_with_items': man_with_items,
        'man': man,
        'vh': vh,
        'users': users,
        'logo': logo,
        'woman_with_comment': woman_with_comment,
        'comment': comment,
        'woman': woman,
        # Images
        'features': features,
        'games': games,
        'faqs': faqs,
    })

def register(request):
    return render(request, 'users/register.html')


def login(request):
    return render(request, 'users/login.html')


def home(request):
    return render(request, 'users/home.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('web:users-home')

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super().form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
