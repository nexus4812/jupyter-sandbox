FROM python:3.9.7-slim
USER root

# apt-get
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \

    # install for matplotlib
    ffmpeg \

    # install for jupyterlab_variableinspector
    nodejs \
    npm

# install dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip  && \
    pip install -r /tmp/requirements.txt

# pip install (extension)
RUN pip install \
    # for jupyterlab_variableinspector
    lckr_jupyterlab_variableinspector==3.0.7 \

    # for jupyterlab-lsp
    jupyterlab-lsp \
    python-language-server[all]

# install jupyter lab extension
RUN jupyter labextension install \
    @lckr/jupyterlab_variableinspector@3.0.7 \
    @krassowski/jupyterlab-lsp

# clean cache(apt-get and pip)
RUN apt-get clean && rm -rf /var/lib/apt/lists/* ~/.cache/pip

WORKDIR "${HOME}"
