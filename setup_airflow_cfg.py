#/etc/airflow/airflow.cfg
import os
from string import Template
import json

HOME = os.environ.get('AIRFLOW_HOME', '/etc/airflow/')
HOME_TEMPLATE = os.environ.get('AIRFLOW_HOME_TEMPLATE', '/etc/airflow_template/')

cfg = 'airflow.cfg.template'

data = None

for fldr in [HOME_TEMPLATE, HOME, './', '/']:
	try:
		with open(cfg, 'rt') as f:
			data = Template(f.read())
		continue
	except:
		pass

assert data is not None, 'data should be none'

params_list = [
	'REDIS_PASSWORD',
	'REDIS_HOST',
	'REDIS_PORT',
	'REDIS_PART',
	'POSTGRES_USER',
	'POSTGRES_PASSWORD',
	'POSTGRES_HOST',
	'POSTGRES_PORT',
	'POSTGRES_DATABASE'
]

save_placeholders = ['FERNET_KEY']

params = {}

for k in params_list:
	params[k] = os.environ.get(k, '')

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

result = data.substitute(params)

try:
	with open(HOME + '/properties.json', 'wt') as f:
		json.dump(params, f)
except:
	pass



with open(HOME + '/' + cfg[:-len('.template')], 'wt') as f:
	f.write(result)

