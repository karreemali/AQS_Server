#!/bin/sh

# install stuff
#sudo apt update
sudo apt install python3-pip\
 python3-dev\
 build-essential\
 libssl-dev\
 libffi-dev\
 python3-setuptools\
 nginx -y

# pull git repo
git clone https://github.com/karreemali/AQS_Server.git
cd AQS_Server
sudo chmod 755 .

# install python requirements
python3 -m pip install -r ~/AQS_Server/requirements.txt

# allow port 5000
sudo apt-get install ufw
sudo ufw enable
sudo ufw allow 5000

# enable gunicorn
sudo gunicorn --bind 0.0.0.0:5000 wsgi:app

# enable service
#sudo touch /etc/systemd/system/AQS_Server.service
sudo cp service.conf /etc/systemd/system/AQS_Server.service
sudo systemctl start AQS_Server
sudo systemctl enable AQS_Server

# enable nginx
sudo cp nginx.conf /etc/nginx/sites-available/AQS_Server
sudo ln -s /etc/nginx/sites-available/AQS_Server /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# allow port nginx
sudo ufw allow 'Nginx Full"
