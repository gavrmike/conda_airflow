export JAVA_HOME=/opt/conda/

python /opt/conda/bin/setup_airflow_cfg.py

[ "${INIT_AIRFLOW:-1}" -eq "1" ] && airflow initdb

/usr/bin/supervisord
