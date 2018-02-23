# flake8:noqa

bind = "127.0.0.1:8000"
threads = 12
logconfig = "{{ hubs_conf_dir }}/logging.ini"
accesslog = "{{ hubs_log_dir }}/access.log"
errorlog = "{{ hubs_log_dir }}/error.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" (%(L)ss)'
