FROM python:3.8-buster

WORKDIR /app

# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y chromium chromium-driver python-selenium

# Now copy in our code, and run it
COPY . /app
