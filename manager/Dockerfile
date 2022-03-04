FROM python:3.7.1

# Setting the working directory for RUN, CMD, COPY etc.
WORKDIR /usr/src/app

# COPY local requirements.txt to working directory.
COPY requirements.txt ./

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Volume 
VOLUME [ "/usr/src/app/data" ]

# Copy the content of the local directory to the working directory.
COPY . .

# Run this command on container start.
CMD [ "python", "./app.py" ]
