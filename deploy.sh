PROJECT_NAME="qvault"

PYTHONPATH=/etc/opt/$PROJECT_NAME:/opt/$PROJECT_NAME \
    /opt/$PROJECT_NAME/venv/bin/python \
    /opt/$PROJECT_NAME/manage.py collectstatic --noinput \
    --settings=settings

PYTHONPATH=/etc/opt/$PROJECT_NAME:/opt/$PROJECT_NAME \
    /opt/$PROJECT_NAME/venv/bin/python \
    /opt/$PROJECT_NAME/manage.py migrate \
    --settings=settings

PYTHONPATH=/etc/opt/$PROJECT_NAME:/opt/$PROJECT_NAME \
    /opt/$PROJECT_NAME/venv/bin/python \
    /opt/$PROJECT_NAME/manage.py compilemessages \
    --settings=settings


/opt/$PROJECT_NAME/venv/bin/python -m compileall \
    /etc/opt/$PROJECT_NAME

sudo systemctl daemon-reload
sudo systemctl restart $PROJECT_NAME
sudo systemctl restart nginx
