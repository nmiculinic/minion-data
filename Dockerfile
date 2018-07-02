FROM python:3

RUN apt-get update && apt-get install -y --no-install-recommends \
        zlib1g \
        libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY --from=nmiculinic/graphmap /usr/bin/graphmap /usr/bin/graphmap

WORKDIR /usr/src/req
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /usr/src/app
COPY . .
RUN python setup.py install
ENTRYPOINT ["python3", "-m", "minion_data"]
