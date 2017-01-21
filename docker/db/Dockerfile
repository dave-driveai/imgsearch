FROM ubuntu:14.04

# DRIVEAI_REGISTRY_IMAGE_NAME: dashboard/online

# mongodb install preparation
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
RUN echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | \
  tee /etc/apt/sources.list.d/mongodb-org-3.0.list

# ubuntu packages
RUN apt-get update && apt-get install -y \
  build-essential \
  git \
  libffi-dev \
  libssl-dev \
  mongodb-org \
  nodejs \
  npm \
  python-dev \
  python-pip \
  python3-pip \
  openssl

# python packages
RUN pip3 install --upgrade pip \
  && pip3 install \
  flask \
  flask-login \
  flask-restful \
  mongoengine \
  pyopenssl

# Define mountable directories.
VOLUME ["/data/db"]

# Define working directory.
WORKDIR /data

# Define default command.
CMD ["mongod"]

# Expose ports.
#   - 27017: process
#   - 28017: http
EXPOSE 27017
EXPOSE 28017
