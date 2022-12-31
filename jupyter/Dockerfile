FROM python:3.11-slim
USER root

# apt-get
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends\
    ffmpeg # install for matplotlib
    # install for jupyterlab_variableinspector
    # nodejs \
    # npm

# install dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# pip install (extension)
#RUN pip install \
#    # show-variable:jupyterlab_variableinspector
#    lckr_jupyterlab_variableinspector==3.0.7 \
#    # code-complete:jupyterlab-lsp
#    jupyterlab-lsp \
#    python-language-server[all] \
#    # format:jupyterlab-code-formatter
#    jupyterlab-code-formatter \
#    black \
#    yapf \
#    isort \
#    autopep8

# install jupyter lab extension
#RUN jupyter labextension install @lckr/jupyterlab_variableinspector@3.0.7
#RUN jupyter labextension install @krassowski/jupyterlab-lsp

# clean cache(apt-get and pip)
RUN apt-get clean && rm -rf /var/lib/apt/lists/* ~/.cache/pip

WORKDIR "${HOME}"
