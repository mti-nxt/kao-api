# -*- coding: utf-8 -*-
import multiprocessing

# Server Socket
bind = 'unix:/tmp/gunicorn/kao-api.sock'
backlog = 2048

# Worker Processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
max_requests = 0
timeout = 30
keepalive = 2
debug = False
spew = False

# Logging
loglevel = 'info'
logconfig = None

# Process Name
proc_name = 'kao-api'