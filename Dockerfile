# Install
FROM ubuntu:18.04 as builder

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt
RUN apt-get update && apt-get install -y \
  python3.7 \
  python3-pip \
  python3-distutils \
  python3-setuptools
  
RUN pip install --upgrade pip
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

# Run
FROM ubuntu:18.04 as base

WORKDIR /app
COPY --from=builder /install /usr/local
COPY _sentiment_doc_2_vec_model.h5 _sentiment_doc_2_vec_vocab.txt app.py utils.py config.py ./

ARG STAGE
ARG SECRET

ENV APP_SETTINGS=${STAGE}
ENV SECRET=${SECRET}

EXPOSE 5000

CMD [ "./venv/bin/python3", "-m", "app.py" ]
