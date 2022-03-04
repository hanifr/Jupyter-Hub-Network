# With this base image: Put yur `jupyterhub_config.py`
# next to your Dockerfile and it will be added to the
# image automatically on build.
FROM jupyterhub/jupyterhub-onbuild:0.9.4

# Adding a user hubadmin with password "adminpw".
# This will be the deffault admin for Jupyterhub (change password!). 
RUN useradd -m hubadmin && \
    echo "hubadmin:adminpw" | chpasswd
    
    
# Copy TLS certificate and key
#ENV SSL_CERT /srv/jupyterhub/secrets/jupyterhub.crt
#ENV SSL_KEY /srv/jupyterhub/secrets/jupyterhub.key
#COPY ./secrets/*.crt $SSL_CERT
#COPY ./secrets/*.key $SSL_KEY
#RUN chmod 700 /srv/jupyterhub/secrets && \
#chmod 600 /srv/jupyterhub/secrets/*

# Install dockerspawner.
RUN /opt/conda/bin/conda clean -tipsy && \
    /opt/conda/bin/pip install --no-cache-dir dockerspawner==0.9.*

COPY ./userlist /srv/jupyterhub/userlist