FROM cfrc2694/uniandes-pheno-code-server:latest

# Clone the repo Phenomenology-group-uniandes/detectors_school_bootcamp
RUN cd /root/ && \ 
    git clone https://github.com/Phenomenology-group-uniandes/detectors_school_bootcamp.git

# Update pip
RUN pip3 install --upgrade pip

# Install pip requirements from the repo
RUN pip3 install -r /root/detectors_school_bootcamp/requirements.txt

# Password for code-server
ENV PASSWORD="my_password"

# Start code-server on port 8080 and use the repo as the working directory
CMD ["code-server", "--auth", "password", "--host", "0.0.0.0" , "--port", "8080", "/root/detectors_school_bootcamp/"   ]