from django.http import HttpResponse
from django.http.response import JsonResponse
import nmap3

import json

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

class NmapScanner(object):

    def perform_full_scan_and_save(self, target, args="-A"):

        nmap = nmap3.Nmap()
        scanner_result = nmap.nmap_version_detection(target, args=args)

        scanner_history = ScannerHistory(
            target=target
        )

        scanner_history.save()

        IPList = []

        # Iterate over scanner result to get each IP and put them inside a list
        # This will enable the access to the objects inside each nested dictionary in scanner_result dictionary

        for hostIP in scanner_result:
            IPList.append(hostIP)

        for IP in IPList:

            host_data = {
                'IP': IP
            }

            """
            Check if key exists in dictionary, source:
            https://stackoverflow.com/a/35485003/9655579

            Check if key is not None, source:
            https://stackoverflow.com/a/2710949/9655579
            """

            if "macaddress" in scanner_result[IP]:

                if scanner_result[IP]["macaddress"] is not None:

                    if "addr" in scanner_result[IP]["macaddress"]:
                        host_data['mac_address'] = scanner_result[IP]["macaddress"]["addr"]

            host, created = Host.objects.get_or_create(**host_data)

            # Add host to scanner history (many to many relation)
            scanner_history.hosts.add(host)

            if "osmatch" in scanner_result[IP]:
                for osmatch in scanner_result[IP]["osmatch"]:

                    operative_system_match, created = OperativeSystemMatch.objects.get_or_create(
                        name=osmatch["name"],
                        accuracy=osmatch["accuracy"],
                        line=osmatch["line"],
                        host=host
                    )

                    if "osclass" in osmatch:
                        operative_system_class, created = OperativeSystemClass.objects.get_or_create(
                            operative_system_match=operative_system_match,
                            type=osmatch["osclass"]["type"],
                            vendor=osmatch["osclass"]["vendor"],
                            operative_system_family=osmatch["osclass"]["osfamily"],
                            operative_system_generation=osmatch["osclass"]["osgen"],
                            accuracy=osmatch["osclass"]["accuracy"]
                        )

            if "ports" in scanner_result[IP]:
                for ports in scanner_result[IP]["ports"]:

                    port, created = Port.objects.get_or_create(
                        protocol=ports["protocol"],
                        portid=ports["portid"],
                        state=ports["state"],
                        reason=ports["reason"],
                        reason_ttl=ports["reason_ttl"],
                        host=host
                    )

                    if "service" in ports:
                        port_service_data = {}

                        port_service_data['port'] = port

                        if "name" in ports["service"]:
                            port_service_data['name'] = ports["service"]["name"]

                        if "product" in ports["service"]:
                            port_service_data['product'] = ports["service"]["product"]

                        if "extrainfo" in ports["service"]:
                            port_service_data['extra_info'] = ports["service"]["extrainfo"]

                        if "hostname" in ports["service"]:
                            port_service_data['hostname'] = ports["service"]["hostname"]

                        if "ostype" in ports["service"]:
                            port_service_data['operative_system_type'] = ports["service"]["ostype"]

                        if "method" in ports["service"]:
                            port_service_data['method'] = ports["service"]["method"]

                        if "conf" in ports["service"]:
                            port_service_data['conf'] = ports["service"]["conf"]

                        port_service, created = PortService.objects.get_or_create(
                            **port_service_data
                        )

        return scanner_history

class ScannerView(View, NmapScanner):
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
        return redirect(reverse('nmap_scanner:form_scanner_view'))
