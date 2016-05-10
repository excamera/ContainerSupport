Dependencies Installation
--------------------------
    pip install docker

Initial Setup
-------------
1. Create a new Docker VM
$ docker-machine create --driver virtualbox default

2. Check if machine is created
$ docker-machine ls

3. Get the environment commands for your new VM.
export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://192.168.99.101:2376"
export DOCKER_CERT_PATH="/Users/mary/.docker/machine/machines/default"
export DOCKER_MACHINE_NAME="default"
# Run this command to configure your shell:
# eval "$(docker-machine env default)"

4. Connect your shell to the default machine.
$ eval "$(docker-machine env default)"

5. Check if hello-world works
$ docker run hello-world

Further help : https://docs.docker.com/engine/installation/mac/
