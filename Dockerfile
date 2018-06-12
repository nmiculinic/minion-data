FROM python:3

WORKDIR /usr/src/req
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /usr/src/app
COPY . .
RUN python setup.py install
ENTRYPOINT ["python3", "-m", "minion_data"]
