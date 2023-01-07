FROM python:3.11-slim
USER root

# apt-get
# install ffmpeg for matplotlib
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends\
    ffmpeg && \
    apt-get clean && rm -rf /var/library/apt/lists/*

# install pip dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    # pip install -e /workspace/  && \
    pip install -r /tmp/requirements.txt  && \
    rm -rf ~/.cache/pip

WORKDIR "${HOME}"
