FROM python:3.12

WORKDIR /giver

COPY requirements.txt .

RUN pip install setuptools
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

COPY config.yaml ./config.yaml

CMD ["python", "__main__.py"]

