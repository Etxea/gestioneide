from django import forms
from localflavor.es.forms import *
from django.forms import ModelForm
from gestioneide.models import *
from django.contrib.auth.models import User

class GrupoCreateForm(ModelForm):
    class Meta:
        model = Grupo
        fields = "__all__" 

class AnotacionGrupoForm(ModelForm):
    class Meta:
        model = AnotacionGrupo
        fields = "__all__"

class EnvioNotasForm(forms.Form):
    group_id = forms.CharField(widget=forms.HiddenInput)
    trimestre = forms.CharField(widget=forms.HiddenInput)
    user_id = forms.CharField(widget=forms.HiddenInput)

class ContactForm(forms.Form):
    title = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    #html = forms.BooleanField()
    group_id = forms.CharField(widget=forms.HiddenInput)
    user_id = forms.CharField(widget=forms.HiddenInput)

    def send_email(self):
        grupo = Grupo.objects.get(id=self.cleaned_data["group_id"])
        for asis in grupo.asistencia_set.all():
            alumno = asis.alumno
            mail = MailAlumno()
            mail.alumno = alumno
            mail.creador = User.objects.get(id=self.cleaned_data["user_id"])
            mail.titulo = self.cleaned_data["title"]
            #Cortamos el mensaje
            resumen_mensaje = self.cleaned_data["message"][:490] + (self.cleaned_data["message"][490:] and '..')
            mail.mensaje = resumen_mensaje
            try:
                from_email=mail.creador.profesor.email
            except:
                from_email=None
            mail.enviado = alumno.enviar_mail(self.cleaned_data['title'],self.cleaned_data['message'],from_email=from_email)
            mail.save()

class GrupoHorarioEmailForm(forms.Form):
    
    message = forms.CharField(widget=forms.Textarea)
    
    group_id = forms.CharField(widget=forms.HiddenInput)
    user_id = forms.CharField(widget=forms.HiddenInput)

    def send_email(self):
        grupo = Grupo.objects.get(id=self.cleaned_data["group_id"])
        context={}
        context['grupo'] = grupo
        year = grupo.year
        context['lista_festivos'] =Festivo.objects.filter(year=year) 
        context['message'] = self.cleaned_data["message"]
        titulo = "Horarios %s"%grupo.year
        mensaje = render_to_string('grupos/email_horario.html', context=context)

        for asis in grupo.asistencia_set.all():
            alumno = asis.alumno    
            mail = MailAlumno()
            mail.alumno = alumno
            mail.creador = User.objects.get(id=self.cleaned_data["user_id"])
            mail.titulo = titulo
            mail.mensaje = mensaje[:490]
            try:
                from_email=mail.creador.profesor.email
            except:
                from_email=None
            mail.enviado = alumno.enviar_mail(titulo,mensaje,from_email=from_email,mensaje_html=True)
            mail.save()


class ContactAlumnoForm(forms.Form):
    title = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    #html = forms.BooleanField()
    asistencia_id = forms.CharField(widget=forms.HiddenInput)
    user_id = forms.CharField(widget=forms.HiddenInput)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        print(self.fields)
        #print("Enviando mail a todos los alumnos del grupo %s"%self.cleaned_data["group_id"])
        asistencia = Asistencia.objects.get(id=self.cleaned_data["asistencia_id"])
        alumno = asistencia.alumno
        mail = MailAlumno()
        mail.alumno = alumno
        mail.creador = User.objects.get(id=self.cleaned_data["user_id"])
        mail.titulo = self.cleaned_data["title"]
        #Cortamos el mensaje
        resumen_mensaje = self.cleaned_data["message"][:490] + (self.cleaned_data["message"][490:] and '..')
        mail.mensaje = resumen_mensaje
        try:
            from_email=mail.creador.profesor.email
        except:
            from_email=None
        mail.enviado = alumno.enviar_mail(self.cleaned_data['title'],self.cleaned_data['message'],from_email=from_email)
        mail.save()
