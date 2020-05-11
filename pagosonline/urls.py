from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


from views import *

urlpatterns = [
    #url(r"^confirmar/(?P<reference>[-\.\w]+)/$", confirm_payment, name="pago_confirmar"),
    url(r"^lista$", login_required(pagos_lista.as_view()), name="pago_lista"),
    url(r"^nuevo/$", login_required(crear_pago_manual.as_view()), name="pago_manual_crear"),
    url(r"^editar/(?P<pk>\d+)/$", login_required(editar_pago_manual.as_view()), name="pago_manual_editar"),
    url(r"^borrar/(?P<pk>\d+)/$", login_required(borrar_pago_manual.as_view()), name="pago_manual_borrar"),
    #url(r"^pago/(?P<pago_id>\d+)/$", pagar_manual, name="pago_manual_pagar"),
    url(r"^pago/(?P<pk>\d+)/$", PagoManual.as_view(), name="pagosonline_manual_pagar"),
    url(r"^(?P<reference>\w+)/(?P<order_id>\d+)/$", make_payment , name="pago"),
    url(r"^confirmar/$", confirm_payment, name="pago_confirmar"),
    url(r"^ok/$", TemplateView.as_view(template_name="pago_ok.html"), name="pago_ok"),
    url(r"^ko/$", TemplateView.as_view(template_name="pago_ko.html"), name="pago_ko"),
]
