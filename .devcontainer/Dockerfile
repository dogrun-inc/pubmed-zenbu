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
    aiohttp==3.8.5 \
    aiosignal==1.3.1 \
    async-timeout==4.0.3 \
    attrs==23.1.0 \
    certifi==2023.7.22 \
    charset-normalizer==3.2.0 \
    frozenlist==1.4.0 \
    idna==3.4 \
    multidict==6.0.4 \
    numpy==1.26.0 \
    openai==0.28.0 \
    pandas==2.1.1 \
    python-dateutil==2.8.2 \
    pytz==2023.3.post1 \
    requests==2.31.0 \
    six==1.16.0 \
    tqdm==4.66.1 \
    tzdata==2023.3 \
    urllib3==2.0.5 \
    yarl==1.9.2 \
    PyYAML==5.1