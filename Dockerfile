FROM jupyter/scipy-notebook

# conda install
USER root

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

USER ${NB_UID}

WORKDIR "${HOME}"
