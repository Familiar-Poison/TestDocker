# Base image
FROM python:3.9

COPY ./Postgres /mnt/app

RUN pip install -r /mnt/app/requirements.txt

RUN apt-get update && apt-get install -y iputils-ping

RUN --mount=type=secret,id=SMTP_USER

# docker build -t python_image https://github.com/Familiar-Poison/TestDocker.git#test

# docker build url#ref:dir where ref is a branch, a tag, or a commit SHA.
# -t = image/tag name
# Github repo needs to be public!