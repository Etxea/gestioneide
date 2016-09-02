# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from models import *
from forms import *

@method_decorator(permission_required('gestioneide.olddatabase_view',raise_exception=True),name='dispatch')
class DbListView(ListView):
    model = OldDatabase
    template_name = 'olddatabase_list.html'

@permission_required('gestioneide.olddatabase_view',raise_exception=True)
def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('importar_list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

@permission_required('gestioneide.olddatabase_view',raise_exception=True)
def load_olddb(request):
    print "Somos load_olddb"
    if request.method == 'POST':
        olddb_id = request.POST.get('id')
        print "Intentando cargar la BBDD con id",olddb_id
        #~ import time
        #~ 
        #~ olddb = OldDatabase.objects.get(id=olddb_id)
        from django.core.management import call_command
        call_command('importacion',olddb_id)
        
        print "Cargar la BBDD con el file",olddb.dbfile
        
        return HttpResponse(
            { 'msg': "hola"},
            content_type="application/json"
        )

@permission_required('gestioneide.olddatabase_add',raise_exception=True)
def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = OldDatabaseForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = OldDatabase(dbfile=request.FILES['dbfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('importar_list'))
    else:
        form = OldDatabaseForm()  # A empty, unbound form

    
    # Render list page with the documents and the form
    return render_to_response(
        'upload.html',
        {'form': form},
        context_instance=RequestContext(request)
    )
