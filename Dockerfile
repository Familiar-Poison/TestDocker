# Base image
FROM python:3.9

COPY ./Postgres /mnt/app

RUN pip install -r /mnt/app/requirements.txt

# docker build -t first_image https://github.com/Familiar-Poison/TestDocker.git#test

# docker build url#ref:dir where ref is a branch, a tag, or a commit SHA.
# -t = image/tag name
# Github repo needs to be public!