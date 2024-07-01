# gunicorn.conf.py

bind = '0.0.0.0:3000'
workers = 4
timeout = 120
loglevel = 'info'
accesslog = '-'
errorlog = '-'
