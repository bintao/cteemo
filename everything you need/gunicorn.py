mport multiprocessing
import os

bind = "0.0.0.0:4000"
workers = multiprocessing.cpu_count()*2 + 1
daemon = True
reload = True
errorlog = os.getcwd()+'/log/error.log'
accesslog = os.getcwd()+'/log/access.log'
loglevel = 'error'
pidfile = os.getcwd()+'/var/gunicorn.pid'
