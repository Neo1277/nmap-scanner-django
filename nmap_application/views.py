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

class ScannerView(View):
    model = ScannerHistory
    template_name = "nmap_application/ad_scanner.html"

    #Get Ad and its comments
    def get(self, request) :
        scanner_history = ScannerHistory.objects.all()
        comment_form = ScannerForm()
        context = {
            'scanner_history' : scanner_history,
            'comment_form': comment_form
        }
        return render(request, self.template_name, context)

    #Get Ad and its comments
    def post(self, request) :
        print(request.POST['target'])
        return redirect(reverse('nmap_scanner:form_scanner_view'))

    def perform_scanning(self, target, args="-A"):
        """This is not ready yet"""
        nmap = nmap3.Nmap()
        scanner_result = nmap.nmap_version_detection(target, args=args)

        IPList = []
        for hostIP in scanner_result:
            IPList.append(hostIP)

        for IP in IPList:
            print( "*************" )
            print( "IP" )
            print( IP )
            print( "*************" )
            """
            Check if key exists in dictionary, source:
            https://stackoverflow.com/a/35485003/9655579
            """
            if "macaddress" in scanner_result[IP]:
                print( "*************" )
                print( "macaddress" )
                print( scanner_result[IP]["macaddress"] )
                print( "*************" )

            if "osmatch" in scanner_result[IP]:
                for hostIP in scanner_result[IP]["osmatch"]:
                    print( "name osmatch" )
                    print( hostIP["name"] )
                    print( hostIP["accuracy"] )
                    print( hostIP["line"] )

                    if "osclass" in hostIP:
                        print( "*************" )
                        print( hostIP["osclass"]["type"] )
                        print( hostIP["osclass"]["vendor"] )
                        print( hostIP["osclass"]["osfamily"] )
                        print( hostIP["osclass"]["osgen"] )
                        print( hostIP["osclass"]["accuracy"] )
                        print( "*************" )

            if "ports" in scanner_result[IP]:
                for hostIP in scanner_result[IP]["ports"]:
                    print( " ports" )
                    print( hostIP["protocol"] )
                    print( hostIP["portid"] )
                    print( hostIP["state"] )
                    print( hostIP["reason"] )
                    print( hostIP["reason_ttl"] )
                    print( hostIP["service"]["name"] )
                    print( hostIP["service"]["method"] )
                    print( hostIP["service"]["conf"] )
                    print( "*************" )

"""
netsh trace start capture=yes

netsh trace stop
"""

"""
def index(request):
    nmap = nmap3.Nmap()
    scanner_result = nmap.nmap_version_detection("192.168.20.*", args="-A")

    print(scanner_result.keys())
    listaIPs = []
    for hostIP in scanner_result:
        listaIPs.append(hostIP)

    for IP in listaIPs:
        print( "*************" )
        print( "IP" )
        print( IP )
        print( "*************" )
        if "macaddress" in scanner_result[IP]:
            print( "*************" )
            print( "macaddress" )
            print( scanner_result[IP]["macaddress"] )
            print( "*************" )

        if "osmatch" in scanner_result[IP]:
            for hostIP in scanner_result[IP]["osmatch"]:
                print( "name osmatch" )
                print( hostIP["name"] )
                print( hostIP["accuracy"] )
                print( hostIP["line"] )

                if "osclass" in hostIP:
                    print( "*************" )
                    print( hostIP["osclass"]["type"] )
                    print( hostIP["osclass"]["vendor"] )
                    print( hostIP["osclass"]["osfamily"] )
                    print( hostIP["osclass"]["osgen"] )
                    print( hostIP["osclass"]["accuracy"] )
                    print( "*************" )

        if "ports" in scanner_result[IP]:
            for hostIP in scanner_result[IP]["ports"]:
                print( " ports" )
                print( hostIP["protocol"] )
                print( hostIP["portid"] )
                print( hostIP["state"] )
                print( hostIP["reason"] )
                print( hostIP["reason_ttl"] )
                print( hostIP["service"]["name"] )
                print( hostIP["service"]["method"] )
                print( hostIP["service"]["conf"] )
                print( "*************" )



    return JsonResponse(scanner_result)
"""

"""
Check if key exists in dictionary, source:
https://stackoverflow.com/a/35485003/9655579
"""