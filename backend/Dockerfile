FROM python:3.10-slim

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock /project/
COPY . /project

WORKDIR /project
RUN pdm install --prod --no-lock --no-editable

EXPOSE 8080
STOPSIGNAL SIGINT

RUN pdm run prisma generate

CMD ["pdm", "prod-server"]