import multiprocessing

authbind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count()*2 + 1
daemon = True
reload = True