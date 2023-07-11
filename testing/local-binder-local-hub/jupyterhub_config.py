"""
A development config to test BinderHub locally.

Run `jupyterhub --config=binderhub_config.py` terminal
Host IP is needed in a few places
"""
import os
import sys
import socket
import yaml
from yaml.loader import SafeLoader

from dockerspawner import DockerSpawner

with open('./configure.yaml') as f:
    config = yaml.load(f, Loader=SafeLoader)

from binderhub.binderspawner_mixin import BinderSpawnerMixin

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
hostip = s.getsockname()[0]
s.close()

# image & token are set via spawn options
class LocalContainerSpawner(BinderSpawnerMixin, DockerSpawner):
    pass

c.JupyterHub.spawner_class = LocalContainerSpawner
c.DockerSpawner.remove = False
c.LocalContainerSpawner.cmd = "jupyter-notebook"
c.LocalContainerSpawner.cors_allow_origin = '*'

c.Application.log_level = "DEBUG"
c.Spawner.debug = True
c.JupyterHub.authenticator_class = "nullauthenticator.NullAuthenticator"

c.JupyterHub.hub_ip = "0.0.0.0"
# note - you may have to replace this directly with the IP as a string :(
c.JupyterHub.hub_connect_ip = config["connect_ip"]

c.JupyterHub.load_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "delete:servers",
        ],
        "services": ["jupyterhub-idle-culler-service"]
    }
]

binderhub_service_name = "binder"
binderhub_config = os.path.join(os.path.dirname(__file__), "binderhub_config.py")
c.JupyterHub.services = [
    {
        "name": binderhub_service_name,
        "admin": True,
        "command": ["python3", "-mbinderhub", f"--config={binderhub_config}"],
        "url": "http://localhost:8585",
        "environment": {
            "JUPYTERHUB_EXTERNAL_URL": config["external_url"],
            "GITHUB_TOKEN": config["github_token"],
            "BANNED_SPECS": config["banned_specs"],
        },
    },
    {
        "name": "jupyterhub-idle-culler-service",
        "command": [
            sys.executable,
            "-m", "jupyterhub_idle_culler",
            "--timeout=3600"
        ]
    }
]
c.JupyterHub.default_url = f"/services/{binderhub_service_name}/"

c.JupyterHub.tornado_settings = {
    "slow_spawn_timeout": 0,
}

c.KubeSpawner.events_enabled = True
