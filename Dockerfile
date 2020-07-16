FROM ubuntu:bionic

# Create Server OS environment
RUN apt-get update -y &&\
    apt-get upgrade -y &&\
    apt-get install python3 -y &&\
    apt-get install python3-pip -y &&\
    apt-get install nginx -y

# App source
COPY . /src
WORKDIR /src

# App dependencies
RUN pip3 install flask
#    pip3 install flask_socketio &&\
#    pip3 install uwsgi


EXPOSE 8080
# App Run
CMD ["python3", "app.py"]