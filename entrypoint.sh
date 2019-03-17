mkdir -p /data/
export PASSWORD=${PASSWORD:-PASSWORD1}
# export PASSWORD_HASH=`echo "$PASSWORD" | python -c "from notebook.auth import passwd; print(passwd(str(input())))"`
export PASSWORD_HASH=`echo -n "'$PASSWORD'" | python -c "from notebook.auth import passwd; print(passwd(str(input())))"`
mkdir $HOME/.jupyter/
echo "c.NotebookApp.password = u'${PASSWORD_HASH}'" > $HOME/.jupyter/jupyter_notebook_config.py
jupyter lab --notebook-dir /data --allow-root --ip 0.0.0.0
