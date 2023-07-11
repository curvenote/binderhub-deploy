source ./configure.sh
echo "Starting Binderhub in Background - this terminal can be closed"
mv nohup.out nohup.out.old
nohup jupyterhub --config=jupyterhub_config.py &
