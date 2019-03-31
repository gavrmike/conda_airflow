export JAVA_HOME=/opt/conda/

python /opt/conda/bin/setup_airflow_cfg.py

airflow initdb

/usr/bin/supervisord
