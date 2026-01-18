from django.shortcuts import render, redirect
from .form import RegistrForm, UserLoginForm
from .models import User
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .token import TokenGenerator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
from django.contrib.auth import login as auth_login, authenticate, logout
# Create your views here.

acc_active_token = TokenGenerator()

def registration(request):
    if request.method != 'POST':
        form = RegistrForm()
    else:
        form = RegistrForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                exist_user = User.objects.get(email = email)
                if not exist_user.is_active:
                    exist_user.delete()
                else:
                    return render(request, "#", {'error' : 'Данный пользователь уже существует'})
            except:
                pass
            
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_domain = get_current_site(request)
            mail_subject = 'Ссылка на активации аккаунта'
            message = render_to_string('auth/acc_active_email.html', {
                'user' : user,
                'domain': current_domain.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': acc_active_token.make_token(user)
            })
            mail = EmailMessage(mail_subject, message, to=[email])
            mail.send()
            return redirect(to='post_list')
    return render(request, 'auth/registration.html', {'form': form})

def activation(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except:
        user = None
    
    if user is not None and acc_active_token.check_token(user, token):
        time_elapsed = timezone.now() - user.date_joined
        if time_elapsed.total_seconds() < 900:
            user.is_active = True
            user.save()
            return render(request, 'auth/success_activate.html')
        else:
            return render(request, 'auth/fail_activate.html')
        
def user_login(request):
    if request.method != 'POST':
        form = UserLoginForm()
    else:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email = form.cleaned_data['email'], password =form.cleaned_data['password'])
            if user is not None:
                auth_login(request, user)
                return redirect(to = 'post_list')
    return render(request, 'auth/login.html', {'form': form})
        
def user_logout(request):
    logout(request)
    return redirect(to = 'post_list')