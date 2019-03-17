FROM continuumio/miniconda3:4.5.12

# spark
RUN conda install -y -c conda-forge -c cyclus java-jdk pyspark==2.3.1 lightgbm xgboost statsmodels scikit-learn jupyterlab catboost bokeh matplotlib sympy seaborn pyhive sqlalchemy pyarrow && pip install h2o

# install hadoop
RUN wget 'http://public-repo-1.hortonworks.com/HDP/debian7/2.x/updates/2.6.4.0/hdp.list' -O /etc/apt/sources.list.d/hdp.list && apt-get update && apt-get install -y python2.7 && ln -s  /usr/bin/python2.7 /usr/bin/python && PATH=/usr/bin/:$PATH apt-get install -y --allow-unauthenticated procps htop hadoop hadoop-hdfs libhdfs0 hadoop-yarn hadoop-mapreduce hadoop-client openssl git vim hive

COPY entrypoint.sh /entrypoint.sh
COPY kinit.sh /opt/conda/bin/kinit.sh

ENTRYPOINT ["bash", "/entrypoint.sh"]
