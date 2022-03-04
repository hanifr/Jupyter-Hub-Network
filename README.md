## How to launch

First change the password in the `adminpw.txt` file.

1. Build the image for the user notebook (the notebook that will be served via jupyterhub to the users).
2. Create the network for jupyterhub, its notebook containers and the database.
3. Create the volume for jupyterhub and its notebooks.
4. Docker-compose build and run.

```
docker build -t jupyterhub-user user-notebook/
docker network create jupyterhub-network
docker volume create --name jupyterhub-data
docker-compose build
docker-compose up -d
```

The names `jupyterhub-user`, `jupyterhub-network` and `jupyterhub_data` are arbitrary. The just have to match the ones in the `.env` file.

## Jupyterhub

Contains `Dockerfile` and `jupyterhub_config.py`. Config defines the notebook image to use (this can be found in `/user-notebook`), the docker-spawner and the Authenticator that works with the `manager`.

## Manager

Used for user management. Flask app that manges user credentials and acts as an authenticator for JupyterHub.

## User notebook

These notebook images are spawned by the Docker-spawner of the JupyterHub. Modify the `user-notebook/Dockerfile` (i.e copy some IPython-Notebooks in the working directory) to cange the notebook that will be launched for every user.

## `.env`

Use this file to set default values for environment variables specified in
docker-compose configuration file. docker-compose will substitute these
values for environment variables in the configuration file IF the variables
are not set in the shell environment.

# Volumes

There will be several volumes `jupyter-user-<username>` volumes and a volume `jupyterhub-data` (in the standard docker volume directory) as well as `manager-data` and `maria-data` in the current (git) directory, after launching the docker-compose.