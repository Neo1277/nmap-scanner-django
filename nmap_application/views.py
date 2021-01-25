from django.http import HttpResponse
import nmap3


def index(request):
    nmap = nmap3.Nmap()
    version_result = nmap.nmap_version_detection("192.168.20.1/24", args="-O -T4")
    print(version_result)
    # print(version_result.keys())
    return HttpResponse(version_result)