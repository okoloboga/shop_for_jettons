FROM python:3.12-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1 
WORKDIR /bot
COPY requirements.txt .
RUN pip install --no-cache -r /bot/requirements.txt
COPY bot /app/__main__.py
CMD ["python", "-m", "bot"]
