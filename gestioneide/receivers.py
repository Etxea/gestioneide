from django.dispatch import receiver

from account.signals import password_changed
from account.signals import user_sign_up_attempt, user_signed_up
from account.signals import user_login_attempt, user_logged_in

from sermepa.signals import payment_was_successful, payment_was_error, signature_error
from matriculas.models import MatriculaEide

from pinax.eventlog.models import log

import logging
log = logging.getLogger("django")

@receiver(user_logged_in)
def handle_user_logged_in(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="USER_LOGGED_IN",
        extra={}
    )


@receiver(password_changed)
def handle_password_changed(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="PASSWORD_CHANGED",
        extra={}
    )


@receiver(user_login_attempt)
def handle_user_login_attempt(sender, **kwargs):
    log(
        user=None,
        action="LOGIN_ATTEMPTED",
        extra={
            "username": kwargs.get("username"),
            "result": kwargs.get("result")
        }
    )


@receiver(user_sign_up_attempt)
def handle_user_sign_up_attempt(sender, **kwargs):
    log(
        user=None,
        action="SIGNUP_ATTEMPTED",
        extra={
            "username": kwargs.get("username"),
            "email": kwargs.get("email"),
            "result": kwargs.get("result")
        }
    )


@receiver(user_signed_up)
def handle_user_signed_up(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="USER_SIGNED_UP",
        extra={}
    )

## SERMEPA

@receiver(payment_was_successful)
def payment_ok(sender, **kwargs):
    log.debug("Somos el evento payment_was_successful gestionado por payment_ok")
    print sender
    reference = sender.Ds_MerchantData
    log.debug("tenemos la referencia: %s"%reference)
    registration_type = reference.split('-')[0]
    registration_id = reference.split('-')[1]
    log.debug( "tenemos una matricula de %s con el id %s"%(registration_type, registration_id))
    r = None
    #Buscamos la matricula 
    if registration_type=="cam":
        log.debug("Es cambridge la buscamos en BBDD")
        r = Registration.objects.get(id=registration_id)
        log.debug("Hemos encontrado el pago manual %s"%r.id)
        log.debug( "Tenemos la matricula/pago, vamos a marcalo como pagado")
        r.set_as_paid()
    elif registration_type=="eide":
        log.debug("Vamos a confirmar un pago EIDE. Lo buscamos en BBDD...")
        r = MatriculaEide.objects.get(id=registration_id)
        r.set_as_paid()

    elif registration_type=="man":
        log.debug("Vamos a confirmar un pago manual. Lo buscamos en BBDD...")
        print Pago.objects.all()
        r = Pago.objects.filter(id=registration_id)
        if len(r)>0:
            log.debug("Hemos encontrado el pago manual %s"%r[0].id)
            log.debug( "Tenemos la matricula/pago, vamos a marcalo como pagado")
            r.set_as_paid()
        else:
            log.debug("Problemas encontrando el pago manual con ID: %s"%registration_id)
    else:
        log.debug( "No sabemos que tipo de matricula es!" )
    

@receiver(payment_was_error)
def payment_ko(sender, **kwargs):
    pass

def sermepa_ipn_error(sender, **kwargs):
    pass

