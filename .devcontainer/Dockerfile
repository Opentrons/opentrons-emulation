# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.209.6/containers/python-3/.devcontainer/base.Dockerfile
ARG USERNAME=root
# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT="3.10-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# Additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libsystemd-dev \
    libudev-dev \
    curl \
    gnupg \
    software-properties-common \
    unzip \
    wget \
    jq

RUN echo alias ls=\'ls -l -a -G --color=auto\' >> /$USERNAME/.bashrc

RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && mkdir /commandhistory \
    && touch /commandhistory/.bash_history \
    && echo $SNIPPET >> "/$USERNAME/.bashrc"

RUN mkdir -p /$USERNAME/.vscode-server/extensions \
        /$USERNAME/.cache \
        /$USERNAME/.local \
        /$USERNAME/commandhistory \
    && chown -R $USERNAME:$USERNAME \
        /$USERNAME/.vscode-server \
        /$USERNAME/.cache \
        /$USERNAME/.local \
        /$USERNAME/commandhistory

ENV POETRY_PATH /$USERNAME/.poetry

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=$POETRY_PATH python - \
    && pip install -U pip pipenv black pylint commitizen

ENV PATH "$POETRY_PATH/bin:$PATH"

COPY . /main_emulation

WORKDIR /main_emulation

RUN make setup
