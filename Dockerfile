FROM python:3.11

WORKDIR /code

# Instala el cliente de Docker dentro de la imagen
RUN apt-get update && apt-get install -y docker.io

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# If running behind a proxy like Nginx or Traefik add --proxy-headers
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
