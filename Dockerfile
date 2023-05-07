ARG BASE_IMAGE=ubuntu:20.04
FROM ${BASE_IMAGE}

ARG PROJECT_NAME=vocal-to-midi
ARG USER_NAME=challenger
ARG GROUP_NAME=challengers
# change this if you want to use your own UID
ARG UID=1001
# change this if you want to use your own GID
ARG GID=1002 
ARG PYTHON_VERSION=3.8
ARG APPLICATION_DIRECTORY=/home/${USER_NAME}/${PROJECT_NAME}
ARG RUN_POETRY_INSTALL_AT_BUILD_TIME="false"

ENV DEBIAN_FRONTEND="noninteractive" \
    LC_ALL="C.UTF-8" \
    LANG="C.UTF-8" \
    PYTHONPATH=${APPLICATION_DIRECTORY}

# Following is needed to install python 3.7
RUN apt update && apt install --no-install-recommends -y software-properties-common 
RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt update && apt install --no-install-recommends -y \
    git curl make ssh openssh-client fish\
    python${PYTHON_VERSION} python3-pip python-is-python3

# Following is needed to swtich default python3 version
# For detail, please check following link https://unix.stackexchange.com/questions/410579/change-the-python3-default-version-in-ubuntu
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1 \
    && update-alternatives --set python3 /usr/bin/python${PYTHON_VERSION} \
    # `requests` needs to be upgraded to avoid RequestsDependencyWarning
    # ref: https://stackoverflow.com/questions/56155627/requestsdependencywarning-urllib3-1-25-2-or-chardet-3-0-4-doesnt-match-a-s
    && python3 -m pip install --upgrade pip setuptools requests \
    && python3 -m pip install poetry

# Add user. Without this, following process is executed as admin. 
# RUN groupadd -g ${GID} ${GROUP_NAME} \
#     && useradd -ms /bin/sh -u ${UID} -g ${GID} ${USER_NAME}
RUN groupadd -g ${GID} ${GROUP_NAME} \
    && useradd -ms /bin/sh -u ${UID} -g ${GID} ${USER_NAME}

USER ${USER_NAME}
WORKDIR ${APPLICATION_DIRECTORY}

# If ${RUN_POETRY_INSTALL_AT_BUILD_TIME} = "true", install Python package by Poetry and move .venv under ${HOME}.
# This process is for CI (GitHub Actions). To prevent overwrite by volume of docker compose, .venv is moved under ${HOME}.
COPY --chown=${UID}:${GID} pyproject.toml poetry.lock ./

# Install Python package by Poetry
RUN poetry install --no-interaction --without dev --no-ansi --no-root -vvv
CMD ["poetry", "run", "streamlit", "run", "src/00_README.py", "--server.port", "8080"]

# copy source code
COPY --chown=${UID}:${GID} ./ ./

EXPOSE 8080
