from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views import View
from .form import UserLoginForm, UserRegistrationForm
from django.urls import reverse_lazy, reverse


# Create your views here.


def login_registration(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    context = {}
    if request.method == 'POST':
        action_type = request.POST.get('action')
        if action_type is None or action_type not in ['login', 'registration']:
            return HttpResponseBadRequest()
        if action_type == 'login':
            registration_form = UserRegistrationForm(initial={'action': 'registration'})
            login_form = UserLoginForm(data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                remember_me_option = login_form.cleaned_data.get('remember_me')
                user = auth.authenticate(username=username, password=password)
                if user:
                    auth.login(request, user)
                    if not remember_me_option:
                        request.session.set_expiry(0)
                    return HttpResponseRedirect(reverse('index'))
        else:
            login_form = UserLoginForm(initial={'action': 'login'})
            registration_form = UserRegistrationForm(data=request.POST)
            if registration_form.is_valid():
                registration_form.save()
                context.update({'success_message': 'Successful registration,'
                                                   ' a confirmation email has been sent'
                                                   ' to your email'})
            else:
                context.update({'register_priority': True})

            print(registration_form.errors)

    else:
        login_form = UserLoginForm(initial={'action': 'login'})
        registration_form = UserRegistrationForm(initial={'action': 'registration'})

    context.update({'login_form': login_form,
                    'registration_form': registration_form}
                   )
    return render(request, 'users/login-register.html', context=context)
