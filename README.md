# MonitoringLabRedes
Final project of the laboratory course networks.

# Docker Basics

Building application with 3 services: Monitor, ServerTcp and Apache Server.

Monitor: Generates Ping-Tests, DNS-Test and GetRequest.

ServerTcp: Saves tests to an html file.

Apache Server: Create an http server to show the tests.

Each service must run in a different container.

# Installation

First of all you need to [install docker](https://docs.docker.com/engine/install/ubuntu/). Go to Oficial page for more details about installation.

# Image

Once you have docker installed, you can get the image of this aplication from my repository on Docker Hub.

- docker pull matheusdutra0207/monitoringlabredes

Or you can build the image.

- docker build --tag=labredes2021 .

# Containers
## Run the container "monitor".

- sudo docker run --rm --network=host --name=monitor matheusdutra0207/monitoringlabredes python3 monitor.py "HostServer" "PortServer" "Domain to Dns-test" "Interval time in secunds of each monitoring"

## For exemple:

- sudo docker run --rm --network=host --name=monitor matheusdutra0207/monitoringlabredes python3 monitor.py 127.0.0.1 8081 google.com 2
  
## Or run the container with your own config file:
  
- sudo docker run --rm --network=host -v "$PWD:/app/config" --name=monitor2 matheusdutra0207/monitoringlabredes python3 monitor.py 127.0.0.1 8081 google.com 2

Obs: The command above must be in the same folder as your config.txt (One exemplo this file are in folder config this same repository).

## Now, in the same folder run the containers "tcpserver" and "my-apache-app".
  
- sudo docker run --rm -p 8081:8081 -v "$(pwd):/app/www" --name=tcpserver matheusdutra0207/monitoringlabredes python3 server.py 8081
  
- sudo docker run -it --rm  --name my-apache-app -p 8080:80 -v "$PWD":/usr/local/apache2/htdocs/ httpd:2.4


 
