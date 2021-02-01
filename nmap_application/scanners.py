import nmap3
from scapy.all import *

from .models import (
    Host,
    OperativeSystemMatch,
    OperativeSystemClass,
    Port,
    PortService,
    ScannerHistory
)

class NmapScanner(object):

    """This method save the data obtained from nmap scan"""
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


class ScapyScanner(object):

    def __init__(self):
        self.target = None

    """This method returns data extracted from arping scan in a List"""
    def perform_quick_scan_and_extract(self):

        # Perform scan (scapy)
        answered, unanswered = arping(self.target)

        data = []

        for row in answered:
            row_string = str(row)

            # Extract data from row separated by character '|'
            columns = row_string.split('|')

            """
            Get string after specific substring, source
            https://stackoverflow.com/a/12572399/9655579
            """
            key_before_ip = "pdst="
            ip_column = columns[1]
            ip = ip_column[ip_column.index(key_before_ip) + len(key_before_ip):]

            key_before_mac = "src="
            mac_column = columns[2]

            mac = mac_column[mac_column.index(key_before_mac) + len(key_before_mac):]
            mac = mac.split('type')
            mac = mac[0].strip()

            data.append(
                {
                    'IP':ip,
                    'mac_address':mac
                }
            )

        return data

    """This method save the data returned from perform_quick_scan_and_extract() method """
    def save_quick_scan(self):

        data = self.perform_quick_scan_and_extract()

        scanner_history = ScannerHistory(
            target=self.target
        )

        scanner_history.save()

        for row in data:
            host, created = Host.objects.get_or_create(
                IP=row['IP'],
                mac_address=row['mac_address']
            )

            # Add host to scanner history (many to many relation)
            scanner_history.hosts.add(host)

        return scanner_history
