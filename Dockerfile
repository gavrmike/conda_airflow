from continuumio/miniconda:4.5.12

RUN conda install -y -c conda-forge pyspark lightgbm xgboost h2o statsmodels scikit-learn jupyterlab catboost bokeh matplotlib sympy seaborn pyhive sqlalchemy && apt-get install -y vim

# install hadoop
RUN wget 'http://public-repo-1.hortonworks.com/HDP/debian7/2.x/updates/2.6.4.0/hdp.list' -O /etc/apt/sources.list.d/hdp.list && apt-get update && apt-get install -y --allow-unauthenticated procps htop hadoop hadoop-hdfs libhdfs0 hadoop-yarn hadoop-mapreduce hadoop-client openssl

RUN apt-get install -y git

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["bash", "/entrypoint.sh"]
