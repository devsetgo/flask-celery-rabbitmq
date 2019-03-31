FROM python:3.7-alpine
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev
MAINTAINER Mike Ryan "mikeryan56@gmail.com"
EXPOSE 5000
# ENV VIRTUAL_HOST sufee-admin.devsetgo.com
# ENV LETSENCRYPT_HOST sufee-admin.devsetgo.com
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-c", "gunicorn_cfg.py", "run:app"]