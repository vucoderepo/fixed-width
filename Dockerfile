# Setting up python
FROM python:alpine AS base
WORKDIR /fixed-width

# Copy required configuration and source code
COPY requirements.txt .
COPY pytest.ini .
COPY setup.py .
COPY spec.json .
COPY generator/ generator/
COPY tests/ tests/

# Install python dependencies
RUN pip install -r requirements.txt

WORKDIR /fixed-width/generator
# command to run on container start
CMD [ "python3", "./generate.py" ]

