import os
port = os.environ.get("SERVER_PORT", 8000)
bind = [f"0.0.0.0:{port}"]
wsgi_app = "Mobilab_Bank.wsgi:application"
accesslog = "server.access.log"
errorlog = "server.error.log"
pidfile = "gunicorn.pid"


