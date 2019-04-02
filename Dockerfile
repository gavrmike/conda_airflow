FROM continuumio/miniconda3:4.5.12

# install hadoop
RUN wget 'http://public-repo-1.hortonworks.com/HDP/debian7/2.x/updates/2.6.4.0/hdp.list' -O /etc/apt/sources.list.d/hdp.list && apt-get update && apt-get install -y python2.7 && ln -s  /usr/bin/python2.7 /usr/bin/python && PATH=/usr/bin/:$PATH apt-get install -y --allow-unauthenticated procps htop hadoop hadoop-hdfs libhdfs0 hadoop-yarn hadoop-mapreduce hadoop-client openssl git vim hive supervisor

# spark
RUN conda install -y -c conda-forge -c cyclus python=3.6 java-jdk pyspark==2.3.1 bokeh matplotlib sympy seaborn pyhive sqlalchemy pyarrow flower airflow[all] psycopg2 tornado=5.0.2 && pip install h2o 

RUN pip install redis unicodecsv hmsclient fire

RUN useradd airflow

RUN mkdir -p /etc/airflow && chown -R airflow /etc/airflow
RUN mkdir -p /etc/airflow_template  && chown -R airflow /etc/airflow_template
RUN mkdir -p /var/log/supervisord  && chown -R airflow /var/log/supervisord 

COPY airflow.cfg.template /etc/airflow_template/airflow.cfg.template
COPY setup_airflow_cfg.py /opt/conda/bin/setup_airflow_cfg.py
COPY entrypoint.sh /entrypoint.sh
COPY kinit.sh /opt/conda/bin/kinit.sh
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN chown -R airflow /etc/supervisor/conf.d/
RUN mkdir -p /home/airflow && chown -R airflow /home/airflow/
RUN mkdir -p /var/log/airflow && chown -R airflow /var/log/airflow/

EXPOSE 8080 5555

USER airflow
ENV AIRFLOW_HOME /etc/airflow/ 

ENTRYPOINT ["bash", "/entrypoint.sh"]
