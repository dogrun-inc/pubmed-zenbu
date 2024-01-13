# Reference: https://github.com/tom-tan/cwl-for-remote-container-template/tree/master

# Get arguments for python version (in this case, python 3.9 image is used)
ARG VARIANT="3.9-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# Install additional packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    r-base \
    r-base-dev 

# upgrade pip & install python packages
RUN pip install \ 
    --upgrade pip \
    requests>=2.31 \
    openai<=0.28.1 \
    PyYAML>=5.1 \
    Pandas>=2.0.0

# Jupyter Notebook Setting
RUN python3 -m ipykernel install --user