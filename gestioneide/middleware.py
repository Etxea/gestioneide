from django.contrib.auth import logout
from django.contrib import messages
import datetime
from django.shortcuts import redirect
from django.conf import settings
from django.db.models import Q
from mensajes.models import Mensaje
#import gestioneide.settings

class SessionIdleTimeout:
    def process_request(self, request):
        if request.user.is_authenticated():
            current_datetime = datetime.datetime.now()
            if ('last_login' in request.session):
                last = (current_datetime - request.session['last_login']).seconds
                if last > settings.SESSION_IDLE_TIMEOUT:
                    logout(request)
            else:
                request.session['last_login'] = current_datetime
        return None

class MessagesMiddleware:
    def process_request(self, request):
        if request.user.is_authenticated():
            unread_messages = Mensaje.objects.filter(destinatario=request.user).filter(leido=False)
            unread_messages_count =  unread_messages.count()
            request.session['unread_messages_count'] = unread_messages_count
            request.session['unread_messages'] = unread_messages

        return None
