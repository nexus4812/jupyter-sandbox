FROM jupyter/scipy-notebook

# conda install
RUN conda remove --name myenv --all
COPY --chown=${NB_UID}:${NB_GID} myenv.yaml /tmp/
RUN conda env update --file /tmp/myenv.yaml

WORKDIR "${HOME}"
