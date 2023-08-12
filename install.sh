#!/bin/sh
sudo apt-get update

# apache/wsgi
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
sudo a2enmod wsgi


# allow port 5000
sudo apt-get install ufw
sudo ufw enable
sudo ufw allow 5000
