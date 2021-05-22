from datetime import datetime
import logging
import time
import sys
import socket
import json


import requests
from icmplib import ping
from nslookup import Nslookup




logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def loadConfigTxt():
    fileConfig = open('config/config.txt', 'r')
    fileConfigAll = [line.split() for line in fileConfig]

    ping_Boolean = False
    dns_Boolean = False
    getRequest_Boolean = False

    return fileConfigAll, ping_Boolean, dns_Boolean, getRequest_Boolean

class ConnectionTestPing:

    def __init__(self, ip):
        self.ip = ip
        self.status = ""

    def pingTest(self):
        pingTest = ping(self.ip, count = 4)

        if pingTest.packet_loss == 0.0:
            self.status = f"Connection Status 'OK' to {self.ip}. date: {datetime.now()}"

        else:
            self.status = f"Connection Status 'Loss' to {self.ip}. date: {datetime.now()}"
        
        return self

class ConnectionTestWeb:

    def __init__(self, httpAddress):
        self.httpAddress = httpAddress
        self.status = ""

    def webTest(self):
        try:
            request = requests.get(self.httpAddress)
            self.status = f"Request Status Code to {self.httpAddress}: '{request.status_code}'. date: {datetime.now()}"
            return self

        except:
            self.status = f"Request Status Code: 'except address error'. date: {datetime.now()}"
            return self
        #gambiarra

class DnsTest:

    def __init__(self, ipDns, domain):
        self.ipDns = ipDns
        self.status = ""
        self.domain = domain
    
    def dnsTest(self):
        dns_query = Nslookup(dns_servers=[self.ipDns])
        ips_record = dns_query.dns_lookup(self.domain)

        if ips_record.response_full != []:
            self.status = f"Dns status 'OK'. {ips_record.response_full[0]}. date: {datetime.now()}"
        
        else:
            self.status = f"Dns status 'Loss'. date: {datetime.now()}"

        return self

# inicio aqui :)        

if len(sys.argv) != 5: 
    print("""Modo de uso:
                python3 monitor.py <host> <port> <domain> <time>
                host - ip do servidor tcp no qual o módulo irá se conectar.
                port - porta do servidor tcp.
                domain - domínio que  irá ser utilizado no teste de DNS.
                time - intervalo para cada monitoramento em segundos.""")
    sys.exit()

logging.info("Initializing...")
host = sys.argv[1]
domain = sys.argv[3]

try:
    port = int(sys.argv[2])
    monitoringTime = int(sys.argv[4])
except:
    logging.info("Invalid parameter")
    sys.exit()

fileConfigAll, ping_Boolean, dns_Boolean, getRequest_Boolean = loadConfigTxt()

addressList = []

for line in fileConfigAll:

    if line == []:
        ping_Boolean = False
        dns_Boolean = False
        getRequest_Boolean = False 

    elif line[0] == 'Ping':
        ping_Boolean = True
        dns_Boolean = False
        getRequest_Boolean = False

    elif line[0] == 'Dns':
        ping_Boolean = False
        dns_Boolean = True
        getRequest_Boolean = False

    elif line[0] == 'GetRequest':
        ping_Boolean = False
        dns_Boolean = False
        getRequest_Boolean = True

    elif ping_Boolean == True:
        addressList.append({"test": "ping", "address": line[0]})
    
    elif dns_Boolean == True:
        addressList.append({"test": "dns", "address": line[0]})
    
    elif getRequest_Boolean == True:
        addressList.append({"test": "req", "address": f'http://{line[0]}'})

while True:
    PingList = []
    DnsTestList = []
    WebTestList = []


    for address in addressList:

        if address["test"] == "ping":
            #address na key address é  um ip
            testPing = ConnectionTestPing(address["address"]).pingTest()
            PingList.append({"host": testPing.ip, "status": testPing.status})

        elif address["test"] == "dns":
            #address na key address é  um ip
            testDns = DnsTest(ipDns = address["address"], domain = domain).dnsTest()
            DnsTestList.append({"host": testDns.ipDns, "status":testDns.status })

        elif address["test"] == "req":
            #address na key address é  um http address
            testWeb = ConnectionTestWeb(address["address"]).webTest()
            WebTestList.append({"host": testWeb.httpAddress, "status": testWeb.status})

    statusMonitor = {"Ping Status": PingList,
                    "Server web Status": WebTestList,
                    "Dns status": DnsTestList
                }

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send:
        try:
            send.connect((host, port))
            b = json.dumps(statusMonitor).encode('utf-8')
            send.sendall(b)
            logging.info("Sent with success. :)")

        except ConnectionRefusedError:
            logging.info("server not found. :(")
    
    time.sleep(monitoringTime)



