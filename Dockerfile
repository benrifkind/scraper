FROM python:3-slim

# For psycopg2. Need gcc to compile psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
# The copy ensures that this layer is only rerun if the the requirements.txt file changes
COPY requirements.txt /app/
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app
