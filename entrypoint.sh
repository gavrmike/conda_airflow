export JAVA_HOME=/opt/conda/

source /opt/conda/bin/activate

python /opt/conda/bin/setup_airflow_cfg.py

mkdir /var/log/airflow
mkdir /var/log/supervisor

rm /etc/airflow/airflow-webserver.pid || true

[ "${INIT_AIRFLOW:-1}" -eq "1" ] && airflow initdb

/usr/bin/supervisord
