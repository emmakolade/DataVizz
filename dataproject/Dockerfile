# base image - this instruction installs the python image into the docker image
FROM python:3.10.6

# this will specify the root directory of the Django app in the container
ENV DockerHOME=/home/app/webapp

# work directory - creates a directory with the specified path assigned to DockerHOME
RUN mkdir -p ${DockerHOME}

# Envrionment Variable - this ensures that the python output is to the terminal without buffering it at first 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# update pip version
RUN  pip install --upgrade pip 

# copy project in the Docker home Directory 
COPY . ${DockerHOME}

# install dependencies
RUN  pip install -r requirements.txt

# port where the django app runs 
EXPOSE 8000

# start server
CMD python manage.py runserver


