
uwsgi = '''\
[uwsgi]
workers=2
chdir={API_ROOT}
module=proj.wsgi:application
master=True
vacuum=True
socket={PROJ_DIR}/logs/uwsgi.sock
pidfile={PROJ_DIR}/logs/uwsgi.pid
daemonize={PROJ_DIR}/logs/uwsgi.log
uwsgi_read_timeout=300
'''

nginx = '''\
worker_processes auto;

pid {PROJ_DIR}/logs/nginx.pid;

error_log {PROJ_DIR}/logs/nginx_error.log error;

include /usr/share/nginx/modules/*.conf;

events {{
  worker_connections 1024;
}}

http {{
  # custom django upstream of uwsgi
  upstream django_api {{
      server unix:///{PROJ_DIR}/logs/uwsgi.sock;
  }}

  sendfile            on;
  tcp_nopush          on;
  tcp_nodelay         on;
  keepalive_timeout   65;
  types_hash_max_size 2048;

  include             /etc/nginx/mime.types;
  default_type        application/octet-stream;

  include /etc/nginx/conf.d/*.conf;

  server {{
    listen {PORT};
    charset     utf-8;
    client_max_body_size 128M;

    access_log {PROJ_DIR}/logs/nginx_access.log;
    error_log {PROJ_DIR}/logs/nginx_error.log error;

    root {APP_ROOT};
    index index.html;

    # django static
    location /static {{
      alias {API_ROOT}/static;
    }}

    # django project
    location /api {{
      uwsgi_pass  django_api;
      include     /etc/nginx/uwsgi_params; 
      uwsgi_read_timeout 1000s;
    }}

    # tools
    location /plugins {{
      alias /data2/www/html/plugins;
    }}
  }}
}}
'''

shell = '''\
cd {PROJ_DIR}

# start
uwsgi --ini {PROJ_DIR}/config/uwsgi.ini
sudo nginx -c {PROJ_DIR}/config/nginx.conf

# stop
# uwsgi --stop {PROJ_DIR}/logs/uwsgi.pid
# sudo nginx -c {PROJ_DIR}/config/nginx.conf -s stop
'''