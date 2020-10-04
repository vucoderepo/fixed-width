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

#RUN tests using pytest
WORKDIR /fixed-width/tests
RUN ["pytest", "-v", "--junitxml=reports/result.xml"]

# Execute python script to generate fixed width and csv files
WORKDIR /fixed-width/generator

# command to run on container start
CMD tail -f /dev/null

