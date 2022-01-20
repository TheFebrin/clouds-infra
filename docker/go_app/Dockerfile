FROM golang:latest

RUN git clone https://github.com/ThreeDotsLabs/wild-workouts-go-ddd-example.git

RUN chmod +x /go/wild-workouts-go-ddd-example/tools/c4/generate.sh

RUN apt update

RUN apt upgrade

RUN apt install -y vim

RUN apt-get install -y plantuml


# docker run -it --name go-app go-app:latest
# cd wild-workouts-go-ddd-example/tools/c4 && ./generate.sh
# docker cp go-app:/go/wild-workouts-go-ddd-example/tools/c4/out/view-trainings.png .