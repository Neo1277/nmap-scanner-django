from django.http import HttpResponse
from django.http.response import JsonResponse
import nmap3

import json

def index(request):
    """
    netsh trace start capture=yes

    netsh trace stop
    """
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



    # print(version_result)
    # print(scanner_result.keys())
    return JsonResponse(scanner_result)