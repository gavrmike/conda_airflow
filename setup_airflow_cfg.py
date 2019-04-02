#/etc/airflow/airflow.cfg
import os
from string import Template
import json

HOME = os.environ.get('AIRFLOW_HOME', '/etc/airflow/')
HOME_TEMPLATE = os.environ.get('AIRFLOW_HOME_TEMPLATE', '/etc/airflow_template') + '/'

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

