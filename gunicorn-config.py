import multiprocessing

bind = "0.0.0.0:4000"
workers = 1  # multiprocessing.cpu_count() * 2 + 1
daemon = True
