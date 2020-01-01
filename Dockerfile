# https://pmac.io/2019/02/multi-stage-dockerfile-and-python-virtualenv/
# Install
FROM python:3.7.6-stretch AS builder

# Always set a working directory
WORKDIR /app
# Sets utf-8 encoding for Python et al
ENV LANG=C.UTF-8
# Turns off writing .pyc files; superfluous on an ephemeral container.
ENV PYTHONDONTWRITEBYTECODE=1
# Seems to speed things up
ENV PYTHONUNBUFFERED=1

# Install OS package dependencies.
# Do all of this in one RUN to limit final image size.
RUN apt-get update && apt-get install -y \
  python3 \
  python3-venv \
  python3-pip

# Setup the virtualenv
RUN python3 -m venv /venv
# or "virtualenv /venv" for Python 2

# Ensures that the python and pip executables used
# in the image will be those from our virtualenv.
ENV PATH="/venv/bin:$PATH"

# Install Python deps
COPY requirements.txt ./
RUN pip3 install --upgrade pip && \ 
  pip install --no-cache-dir -r requirements.txt

# ---

# Run
FROM python:3.7.6-slim-stretch AS app

# Extra python env
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ARG STAGE
ARG SECRET

ENV APP_SETTINGS=${STAGE}
ENV SECRET=${SECRET}

WORKDIR /app
EXPOSE 5000

# copy in Python environment
COPY --from=builder /venv /venv
COPY _sentiment_doc_2_vec_model.h5 _sentiment_doc_2_vec_vocab.txt app.py utils.py config.py ./

CMD ["/venv/bin/python","app.py"]