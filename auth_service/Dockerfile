FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR 1

WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install --upgrade pip --no-cache-dir --use-feature=fast-deps
RUN pip install -r requirements.txt
COPY . /app/

CMD python manage.py runserver 0.0.0.0:8000
