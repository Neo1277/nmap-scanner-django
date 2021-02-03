# Network scanner #

This Django application uses nmap3 python library to scan the network with the option -A and -sV, this web application also includes the option to perform a quick scan with arping (scapy python library) and after performing the scan, it saves the data into a SQLite3 database. The scan is performed from a form and the data is shown on views that have HTML tables created with bootstrap 4.

## Programming languages (frameworks, libraries) ##
*   Python libraries: nmap3 and scapy
*   Django (Django templates, Django models, crispy forms)

## Database ##
*   SQLite3

## Installation ##
*   In order to use the nmap Python library, Nmap has to be installed on your system, if you don't have Nmap installed on your system, you can find a guide [here](https://nmap.org/download.html "downloadNmap")
*   Create a virtual enviroment for the django dependencies [Link official documentation](https://docs.djangoproject.com/en/3.1/intro/contributing/#getting-a-copy-of-django-s-development-version "djangoenviroment")
*   Activate the enviroment and go to the nmap-scanner-django folder and install the Django dependencies with the following command using the requirements.txt file which has the dependencies
	* ### `pip install -r requirements.txt`
*   To create the the database and tables, on the nmap-scanner-django folder run the following commands (python or python3 depends on your configuration when the enviroment variable on the system was set up)
	* ### `python manage.py makemigrations`
	* ### `python manage.py migrate`

## How to run it ##
*   Go to the nmap-scanner-django folder and run
	* ### `python manage.py runserver`
*   The url where the form to perform the scan is located is: network-scanner ,so the url would be http://127.0.0.1:8000/network-scanner/
*   The links that take you to the views to see the scanner history are below the form
*   To perform the scan, in the form, you have to provide a range of IPs that are going to be scanned, for example: 192.168.40.1/24
*   The IP that I used as an example is an access point, the most common is that the access point is the same local IP of your device and the last number would be 1.