FROM docker.drive.ai/driveai

RUN wget https://storage.googleapis.com/golang/go1.7.4.linux-amd64.tar.gz \
  && sudo tar -C /usr/local -xzf go1.7.4.linux-amd64.tar.gz


ENV GOPATH="/lib/go"
ENV PATH="lib/go/bin:/usr/local/go/bin:${PATH}"

RUN go get github.com/chrislusf/seaweedfs/weed

EXPOSE 9333
EXPOSE 8081