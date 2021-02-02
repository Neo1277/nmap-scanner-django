from django.http import HttpResponse
from django.http.response import JsonResponse

from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from .forms import ScannerForm

from .models import (
    Host,
    OperativeSystemMatch,
    OperativeSystemClass,
    Port,
    PortService,
    ScannerHistory
)

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse, resolve
from django.views import View

from .scanners import NmapScanner, ScapyScanner

class ScannerView(View, NmapScanner, ScapyScanner):

    model = ScannerHistory
    template_name = "nmap_application/scanner_form.html"

    def get(self, request) :

        scanner_form = ScannerForm()

        context = {
            'scanner_form': scanner_form
        }

        return render(request, self.template_name, context)

    def post(self, request) :

        target = request.POST['target']
        type = request.POST['type']

        if type == 'QS':
            self.target = target
            self.save_quick_scan()
        else:
            self.perform_full_scan_and_save(request.POST['target'])

        return redirect(reverse('network_scanner:form_scanner_view'))

class ScannerHistoryListView(ListView):

    model = ScannerHistory
    template_name = "nmap_application/scanner_history_list.html"

    def get(self, request, type) :

        scanner_history = ScannerHistory.objects.filter(type=type)

        context = {
            'scanner_history' : scanner_history
        }
        return render(request, self.template_name, context)

class HostListView(ListView):

    model = Host
    template_name = "nmap_application/scanner_history_host_list.html"

    def get(self, request, scanner_history_id):

        scanner_history = ScannerHistory.objects.get(pk=scanner_history_id)

        hosts = Host.objects.filter(host_history=scanner_history_id)

        context = {
            'hosts' : hosts,
            'scanner_history': scanner_history
        }
        return render(request, self.template_name, context)

# Useful link: base commands
# https://stackoverflow.com/a/3037137/9655579
