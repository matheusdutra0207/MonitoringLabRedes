from socket import socket, AF_INET, SOCK_STREAM
import json
import sys
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def saveHtml(listStatus, adr):
    listStatusInv = reversed(listStatus) # Para mostrar o monitoramento do último para o primeiro.
    with open("www/index.html", "w") as out:
        out.write(f'<h1 style="color: blue; text-align: center"> Trabalho de redes </h1>\n')

    for element in listStatusInv:
        with open("www/index.html", "a") as out:
            out.write(f'<h2 style="color: black; text-align: center"> Monitoring from {adr[0]} </h2>\n')        
        for key, value in element.items():
            if key == "Ping Status":
                for pingTest in value:
                    # cada elemento de pingTest vai ser um dict de cada teste de ping feito no monitor
                    for key_hostStatus, value_hostStatus in pingTest.items():
                        if key_hostStatus == "status":
                            with open("www/index.html", "a") as out:
                                out.write(f'<p style="color: red; text-align: center"> {value_hostStatus} </p>\n')


            if key == "Server web Status":
                for webTest in value:
                    # cada elemento de webTest vai ser um dict de cada teste web feito no monitor
                    for key_hostStatus, value_hostStatus in webTest.items():
                        if key_hostStatus == "status":
                            with open("www/index.html", "a") as out:
                                out.write(f'<p style="color: green; text-align: center"> {value_hostStatus} </p>\n')

            if key == "Dns status":
                for dnsTest in value:
                    # cada elemento de dnsTest vai ser um dict de cada teste de dns feito no monitor
                    for key_hostStatus, value_hostStatus in dnsTest.items():
                        if key_hostStatus == "status":
                            with open("www/index.html", "a") as out:
                                out.write(f'<p style="color: black; text-align: center"> {value_hostStatus} </p>\n')

        with open("www/index.html", "a") as out:
            out.write(f'<br>\n')

class ServerSocket:
    statusList = []

    def __init__(self, host = '0.0.0.0', port = 8082):
        self.host = host
        self.port = port 
    
    def receivePackages(self):
        while True:
            mensage = self.con.recv(1024) 
            if mensage == b'':
                break
            statusMonitor = json.loads(mensage.decode('utf-8'))
            self.statusList.append(statusMonitor)

            if len(self.statusList) > 5: #limitar o tamanho de monitoramentos exibidos no html
                self.statusList.pop(0)

            saveHtml(self.statusList, self.adr)

            logging.info(f'save ok: {self.port}')

    def listen(self):
        logging.info(f'Tcp server Listening on: {self.port}')
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(1)
        while True:
            self.con, self.adr = self.server.accept()
            self.receivePackages()

if len(sys.argv) != 2: 
    print("Inform the server port")
    sys.exit()
try:
    port = int(sys.argv[1])

except:
    print("server port must be interer")
    sys.exit()


TCPserver = ServerSocket(port = port)
TCPserver.listen()