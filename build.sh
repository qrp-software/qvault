PROJECT_NAME="qvault"
PROJECT_USER_NAME="qvault_user"
DOMAIN_NAME="qvault.qrp.com.tr"
PROJECT_PORT=8044

adduser --system --home=/var/opt/$PROJECT_NAME \
    --no-create-home --disabled-password --group \
    --shell=/bin/bash $PROJECT_USER_NAME

/opt/$PROJECT_NAME/venv/bin/python -m compileall \
    -x /opt/$PROJECT_NAME/venv/ /opt/$PROJECT_NAME

/opt/$PROJECT_NAME/venv/bin/python -m compileall \
    -x /opt/$PROJECT_NAME/venv/ /opt/$PROJECT_NAME

mkdir -p /var/opt/$PROJECT_NAME
chown $PROJECT_USER_NAME /var/opt/$PROJECT_NAME

mkdir -p /var/log/$PROJECT_NAME
chown $PROJECT_USER_NAME /var/log/$PROJECT_NAME

mkdir /etc/opt/$PROJECT_NAME
cat << EOF > /etc/opt/$PROJECT_NAME/settings.py
from $PROJECT_NAME.settings.prod import *
EOF

mkdir -p /var/cache/$PROJECT_NAME/static

mkdir /var/opt/$PROJECT_NAME/media
chown $PROJECT_USER_NAME /var/opt/$PROJECT_NAME/media

chgrp $PROJECT_USER_NAME /etc/opt/$PROJECT_NAME
chmod u=rwx,g=rx,o= /etc/opt/$PROJECT_NAME

/opt/$PROJECT_NAME/venv/bin/python -m compileall \
    /etc/opt/$PROJECT_NAME

cat << EOF > /etc/nginx/sites-available/$DOMAIN_NAME
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN_NAME www.$DOMAIN_NAME;
    root /var/www/$DOMAIN_NAME;
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/$PROJECT_NAME.sock;
    }
    location /static/ {
        alias /var/cache/$PROJECT_NAME/static/;
    }
    location /media/ {
        alias /var/opt/$PROJECT_NAME/media/;
    }
}
EOF

ln -s /etc/nginx/sites-available/$DOMAIN_NAME /etc/nginx/sites-enabled/$DOMAIN_NAME


cat << EOF > /etc/systemd/system/$PROJECT_NAME.socket
[Unit]
Description=gunicorn socket
[Socket]
ListenStream=/run/$PROJECT_NAME.sock
[Install]
WantedBy=sockets.target
EOF

cat << EOF > /etc/systemd/system/$PROJECT_NAME.service
[Unit]
Description=personinfo
Requires=$PROJECT_NAME.socket
After=network.target

[Service]
User=$PROJECT_USER_NAME
Group=$PROJECT_USER_NAME
Environment="PYTHONPATH=/etc/opt/$PROJECT_NAME:/opt/$PROJECT_NAME"
Environment="DJANGO_SETTINGS_MODULE=settings"
ExecStart=/opt/$PROJECT_NAME/venv/bin/gunicorn \
    --workers=4 \
    --log-file=/var/log/$PROJECT_NAME/gunicorn.log \
    --bind=localhost:$PROJECT_PORT --bind=[::1]:$PROJECT_PORT \
    $PROJECT_NAME.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

service nginx reload
systemctl enable $PROJECT_NAME.socket
systemctl restart nginx

