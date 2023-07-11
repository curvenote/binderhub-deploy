source ./configure.sh
echo "Starting Binderhub in Terminal - terminal must stay open"
jupyterhub --config=jupyterhub_config.py &
