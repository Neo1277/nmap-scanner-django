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

from django.db.models import F

from django.http import HttpResponse

import json
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
        response = {}

        if type == 'QS':
            self.target = target
            self.save_quick_scan()
            response['success'] = True
        else:
            self.perform_full_scan_and_save(request.POST['target'])
            response['success'] = True

        return HttpResponse(json.dumps(response), content_type="application/json")
        # return redirect(reverse('network_scanner:form_scanner_view'))

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

class OperativeSystemMatchListView(ListView):

    model = OperativeSystemMatch
    template_name = "nmap_application/scanner_history_host_os_matches_list.html"

    def get(self, request, scanner_history_id, host_id):

        host = Host.objects.get(pk=host_id)

        """
        Denormalizing tables

        INNER JOIN, source: 
        https://stackoverflow.com/a/21360352/9655579

        Set alias for fields, source: 
        https://stackoverflow.com/a/46471483/9655579
        """
        operative_system_match = OperativeSystemMatch.objects.filter(
            host=host_id
        ).values(
            'id',
            'name',
            'accuracy',
            'line',
            'created_on',
            'os_match_class__type',
            'os_match_class__vendor',
            'os_match_class__operative_system_family',
            'os_match_class__operative_system_generation',
            'os_match_class__accuracy'
        ).annotate(
            os_id=F('id'),
            os_name=F('name'),
            os_accuracy=F('accuracy'),
            os_line=F('line'),
            os_created_on=F('created_on'),
            os_match_class_type=F('os_match_class__type'),
            os_match_class_vendor=F('os_match_class__vendor'),
            os_match_class_operative_system_family=F('os_match_class__operative_system_family'),
            os_match_class_operative_system_generation=F('os_match_class__operative_system_generation'),
            os_match_class_accuracy=F('os_match_class__accuracy'),
        )

        context = {
            'operative_system_matches' : operative_system_match,
            'host': host,
            'scanner_history_id': scanner_history_id
        }

        return render(request, self.template_name, context)


class PortListView(ListView):

    model = Port
    template_name = "nmap_application/scanner_history_host_ports.html"

    def get(self, request, scanner_history_id, host_id):

        host = Host.objects.get(pk=host_id)

        """
        Denormalizing tables

        INNER JOIN, source: 
        https://stackoverflow.com/a/21360352/9655579

        Set alias for fields, source: 
        https://stackoverflow.com/a/46471483/9655579
        """
        ports = Port.objects.filter(
            host=host_id
        ).values(
            'id',
            'protocol',
            'portid',
            'state',
            'reason',
            'reason_ttl',
            'created_on',
            'port_service__name',
            'port_service__product',
            'port_service__extra_info',
            'port_service__hostname',
            'port_service__operative_system_type',
            'port_service__method',
            'port_service__conf'
        ).annotate(
            port_id=F('id'),
            port_name=F('protocol'),
            port_accuracy=F('portid'),
            port_state=F('state'),
            port_reason=F('reason'),
            port_reason_ttl=F('reason_ttl'),
            port_created_on=F('created_on'),
            port_service_name=F('port_service__name'),
            port_service_product=F('port_service__product'),
            port_service_extra_info=F('port_service__extra_info'),
            port_service_hostname=F('port_service__hostname'),
            port_service_operative_system_type=F('port_service__operative_system_type'),
            port_service_method=F('port_service__method'),
            port_service_conf=F('port_service__conf'),
        )

        context = {
            'ports' : ports,
            'host': host,
            'scanner_history_id': scanner_history_id
        }

        return render(request, self.template_name, context)


# Useful link: base commands
# https://stackoverflow.com/a/3037137/9655579
