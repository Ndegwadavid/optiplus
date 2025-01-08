# newsletter/views.py
from django.shortcuts import redirect
from django.contrib import messages
from .models import Subscriber

def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Successfully subscribed to our newsletter!')
            else:
                messages.info(request, 'You are already subscribed to our newsletter.')
        else:
            messages.error(request, 'Please provide a valid email address.')
    return redirect(request.META.get('HTTP_REFERER', '/'))