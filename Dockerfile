FROM python:3

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt && python setup.py install
ENTRYPOINT ["python3", "-m", "minion_data"]
