# pip installするだけなので、alpineに変更したい。
FROM python:3.7.13-slim
USER root

# install dependencies
COPY ../requirements.txt /tmp/
RUN pip install --upgrade pip  && \
    pip install -r /tmp/requirements.txt -t ${HOME}/vendor

# clean cache for pip
RUN rm -rf /var/lib/apt/lists/* ~/.cache/pip

WORKDIR "${HOME}"
