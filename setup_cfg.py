#/etc/airflow/airflow.cfg
import os
from string import Template
import json

HOME = os.environ.get('AIRFLOW_HOME', '/etc/airflow/')
HOME_TEMPLATE = os.environ.get('AIRFLOW_HOME_TEMPLATE', '/etc/airflow_template') + '/'

DST_SUPERVISOR_CONF = "/etc/supervisor/conf.d/supervisord.conf"

CFG_HEAD = """
[unix_http_server]
file=/tmp/supervisor.sock                       ; path to your socket file

[supervisord]
logfile=/var/log/supervisor/supervisord.log    ; supervisord log file
logfile_maxbytes=50MB                           ; maximum size of logfile before rotation
logfile_backups=10                              ; number of backed up logfiles
loglevel=error                                  ; info, debug, warn, trace
pidfile=/var/run/supervisord.pid                ; pidfile location
nodaemon=true                                   ; run supervisord as a daemon
minfds=1024                                     ; number of startup file descriptors
minprocs=200                                    ; number of process descriptors
user=root                                       ; default user
childlogdir=/var/log/supervisor/               ; where child log files will live

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///tmp/supervisor.sock         ; use a unix:// URL  for a unix socket

; This is where you run individual Tornado instances.
; We run four; one per processor core.
; In development, we ran as many as four per core with no issues.
; If you're looking to minimize cpu load, run fewer processes.
; BTW, Tornado processes are single threaded.
; To take advantage of multiple cores, you'll need multiple processes.
"""

program = """
[program:{name}]
command={command}
stderr_logfile = /var/log/supervisor/{name}.err.log
stdout_logfile = /var/log/supervisor/{name}.out.log
autorestart=true
"""

programs = {
	'kinit': '/bin/bash /opt/conda/bin/kinit.sh',
	'web': 'opt/conda/bin/airflow webserver -p 8080',
	'scheduler': '/opt/conda/bin/airflow scheduler',
	'flower': '/opt/conda/bin/airflow flower',
	'worker1': '/opt/conda/bin/airflow worker -cn worker1 ' + os.environ.get('WORKER1_EXTRA_ARGS', ''),
	'worker2': '/opt/conda/bin/airflow worker -cn worker2 ' + os.environ.get('WORKER2_EXTRA_ARGS', ''),
}

def create_program(name, command):
	return program.format(name=name, command=command)

try:
	with open(DST_SUPERVISOR_CONF, "wt") as f:
		commands = os.environ.get('PROGRAM', 'kinit,web,scheduler,flower,worker1')
		f.write(CFG_HEAD)
		f.write("\n")
		for command in commands.split(','):
			print('add to supervisord', command)
			f.write(create_command(command, programs[command]))
			f.write("\n")
except:
	pass

cfg = 'airflow.cfg.template'

data = None

for fldr in [HOME_TEMPLATE, HOME, './', '/']:
	try:
		with open(fldr + cfg, 'rt') as f:
			data = Template(f.read())
		continue
	except:
		pass

assert data is not None, 'data should be none'

save_placeholders = ['FERNET_KEY']

params = {}

params['HOSTNAME_PORT'] = 'localhost:8080'

for k in os.environ:
	if k.startswith('AIRFLOW_'):
		params[k[8:]] = os.environ.get(k, '')
		print('found:', k[8:])

from cryptography.fernet import Fernet
FERNET_KEY = Fernet.generate_key().decode()

params['FERNET_KEY'] = FERNET_KEY

serialized_properties = {}
try:
	with open(HOME + '/properties.json', 'rt') as f:
		serialized_properties = json.load(f)
except:
	pass

for k, v in serialized_properties.items():
	if k in save_placeholders:	
		params[k] = v
		print('overwrite:', k)

result = data.substitute(params)

try:
	with open(HOME + '/properties.json', 'wt') as f:
		json.dump(params, f)
except:
	pass



with open(HOME + '/' + cfg[:-len('.template')], 'wt') as f:
	f.write(result)

