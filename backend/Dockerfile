FROM python:3.9-slim AS builder

RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY pyproject.toml pdm.lock /project/

WORKDIR /project
RUN pdm export -o requirements.txt


FROM tiangolo/uvicorn-gunicorn:python3.9

ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app
