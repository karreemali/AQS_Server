#!/bin/sh
sudo apt-get update

# install stuff
sudo apt update
sudo apt install python3-pip\
 python3-dev\
 build-essential\
 libssl-dev\
 libffi-dev\
 python3-setuptools\
 nginx\
 wheel -y

# pull git repo
git clone https://github.com/karreemali/AQS_Server.git

# install python requirements
cd AQS_Server
python3 -m pip install -r- requirements.txt

# enable gunicorn
gunicorn --bind 0.0.0.0:5000 wsgi:app

# enable service
cp service.conf /etc/systemd/system/AQS_Server.service
systemctl start AQS_Server
systemctl enable AQS_Server

# enable nginx
cp nginx.conf /etc/nginx/sites-available/AQS_Server
ln -s /etc/nginx/sites-available/AQS_Server /etc/nginx/sites-enabled
nginx -t
systemctl restart nginx

# allow port 5000
apt-get install ufw
ufw enable
ufw allow 5000
ufw allow 'Nginx Full"
