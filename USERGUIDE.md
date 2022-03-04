## After installation
An installation guide is provided in the README.md file inside the project folder.

- **start platform:**  
`docker-compose up -d`
Starts containers for MariaDB, JupyterHub and the usermanager. The -d option runs the containers in the background.

- **stop platform:**  
`docker-compose down`
Shuts down all running containers of the platform.

- **access usermanager:**  
The usermanager runs locally on port 5000. To access the user interface, go to the address 127.0.0.1:5000 in a browser.
The admin username is "hubadmin", the password was chosen before the installation.

- **access JupyterHub:**  
The JupyterHub runs locally on port 8080. To access the user interface, go to the address 127.0.0.1:8080 in a browser.
You can log in with credentials saved in the usermanager. By default, JupyterHub navigates to the Jupyter Notebook tree after login but if you prefer working with JupyterLab, you can replace the "tree" in the url by "lab".