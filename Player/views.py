from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Player
from django.contrib import messages
from .forms import PlayerCreationForm, LoginForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm
from levelrecord.models import ClassicLevelRecord
from django.db.models import Q
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data['username']
                password=form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("home")
                else:
                    messages.error(request, ("Incorrect credentials. Please try again."))
        else:
            form = LoginForm()

        return render(request, 'player/login.html', {'form': form})
    
def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out."))
    
    return redirect("player:login")

def register_user(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            form = PlayerCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, ("Registration successful. An email has been sent with instructions to verify your account."))
                return redirect("player:verify-email")
        else:
            form = PlayerCreationForm()

        return render(request, 'player/register.html', {'form': form})

def verify_email(request):
    if not request.user.is_email_verified:
        current_site = get_current_site(request)
        user = request.user
        email = request.user.email
        subject = "Verify your email"
        message = render_to_string('player/emailbody.html', {
            'request': request,
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        email = EmailMessage(
            subject, message, to=[email]
        )
        email.content_subtype = 'html'
        email.send()
        return redirect('player:profile', username=request.user.username)
    else:
        return redirect('player:profile', username=request.user.username)

def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Player.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Player.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('player:profile', username=request.user.username)  
    else:
        messages.warning(request, 'The link is invalid.')
    return redirect('player:profile', username=request.user.username)

class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'player/passwordreset.html'
    email_template_name = 'player/passwordresetbody.html'
    success_url = reverse_lazy('player:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "We have emailed you instructions for setting your password. If you don't receive an email, please make sure you've entered the address you registered with, and check your spam folder.")
        return redirect('player:login')

class CustomPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'player/passwordresetconfirm.html'
    success_url = reverse_lazy('player:password_reset_complete')
    success_message = "Your password has been set. You can now log in with the new password."

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Your password has been set. You can now log in with the new password.")
        return redirect('player:login')

def profile(request, username):
    player = Player.objects.get(username=username)

    player_ranking = Player.objects.filter(classic_points__gt=player.classic_points).count() + 1
    beaten_levels = ClassicLevelRecord.objects.filter(player=player)
    hardest_level = beaten_levels.order_by('level__ranking').first()
    first_victors = [record for record in beaten_levels if record.level.first_victor == player]
    level_counts = {
      'main': beaten_levels.filter(level__ranking__lte=75).count(),
      'extended': beaten_levels.filter(Q(level__ranking__gt=75) & Q(level__ranking__lte=150)).count(),
      'legacy': beaten_levels.filter(level__ranking__gt=150).count()
    }

    context = {
        'player': player,
        'player_ranking': player_ranking,
        'beaten_levels': beaten_levels,
        'hardest_level': hardest_level,
        'first_victors': first_victors,
        'level_counts': level_counts,
    }

    return render(request, 'player/profile.html', context)