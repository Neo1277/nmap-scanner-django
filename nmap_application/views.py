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
from django.urls import reverse_lazy, reverse
from django.views import View

from .scanners import NmapScanner, ScapyScanner

class ScannerView(View, NmapScanner, ScapyScanner):
    model = ScannerHistory
    template_name = "nmap_application/ad_scanner.html"

    def get(self, request) :
        scanner_history = ScannerHistory.objects.all()
        scanner_form = ScannerForm()
        context = {
            'scanner_history' : scanner_history,
            'scanner_form': scanner_form
        }
        return render(request, self.template_name, context)

    def post(self, request) :
        print(request.POST['target'])
        self.perform_full_scan_and_save(request.POST['target'])
        # self.target = request.POST['target']
        # self.save_quick_scan()
        return redirect(reverse('nmap_scanner:form_scanner_view'))
