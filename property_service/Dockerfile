FROM python:3.11-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
    && pip install --no-cache-dir --upgrade pip
    
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir --requirement /app/requirements.txt

COPY . /app

EXPOSE 8002

# # Run manage.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]