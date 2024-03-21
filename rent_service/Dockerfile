FROM python:3.11-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
    && pip install --no-cache-dir --upgrade pip
    
# Define environment variable
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir --requirement /app/requirements.txt

COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8008

# # Run manage.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8008"]