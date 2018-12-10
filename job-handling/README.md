# Spawn workers in Kubernetes interacting with RabbitMQ

Using similar structure but made changes as and when required
https://kubernetes.io/docs/tasks/job/coarse-parallel-processing-work-queue/

# Introduction:
    In this example we will create a rabbitmq replication controller and a Kubernetes [Job](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/)  which handles 2 messages in parallel, spawning new "PODS" with each message. The PODS reads messages from the rabbitmq server and sends acknowledgement back.

    We will use a temporary container which acts as a client which sends message to rabbitmq as needed.

# Pre-reqs

1.  Using custom rabbitmq server:
    The default rabbitmq docker image needs to have some settings changed
    ```
    [{rabbit,[{loopback_users, []},{channel_max,0}]}]
    ```
    For this example to work flawlessly.

2.  Using Pika (python3 library) to get messages from rabbitmq server


# Steps to reproduce

1.  Create the Rabbitmq service and controller

    ```
    kubectl create -f ./rabbitmq-service.yaml
    kubectl create -f ./rabbitmq-controller.yaml
    ```

2.  Create a temp container which acts as client. We will exec into it as needed and send messages to rabbitmq server.
    In Real world this can be a web service which sends messages to rabbitmq server.

    ```
    kubectl run -i --tty temp --image ubuntu:18.04

    // after exec into container

    # apt-get update
    # apt-get install -y curl ca-certificates amqp-tools python dnsutils

    // verify if rabbitmq service is reachable
    # nslookup rabbitmq-service

    // create a env variable for future use.
    # export BROKER_URL=amqp://guest:guest@rabbitmq-service:5672

    // to test rabbitmq functionality run the commands below (optional)

    # /usr/bin/amqp-declare-queue --url=$BROKER_URL -q foo -d
    foo

    # Publish one message to it:

    # /usr/bin/amqp-publish --url=$BROKER_URL -r foo -p -b Hello

    # And get it back.

    # /usr/bin/amqp-consume --url=$BROKER_URL -q foo -c 1 cat && echo
    Hello
    #
    ```
    Keep this terminal running.


3.  Worker is defined in ./worker-image/worker.py, it used PIKA to read messages from the rabbitmq service. The Dockerfile will create a image which can then be pushed to docker hub or google container registry.
    In another terminal
    ```
    # cd  worker-image
    # docker build . --tag job-wq-1
    # docker tag job-wq-1 srini92/job-wq-1
    # docker push srini92/job-wq-1

    use your own docker hub repo and make appropriate changes in job.yaml
    ```

4.  In ./job.yaml we define a kubernetes job which has specification to run 2 jobs in parallel and exit job after 8 of them are completed.

    ```
    # sudo kubectl create -f ./job.yaml
    ```

  It should all fall into place now.

5.  Once the job is running make sure the pods are spawned (but no work is being done because there is no messages in rabbitmq)
    Lets insert some jobs, going back to terminal in step 2

    ```
    # /usr/bin/amqp-declare-queue --url=$BROKER_URL -q job1  -d
    # for f in apple banana cherry date fig grape lemon melon
    > do
    >   /usr/bin/amqp-publish --url=$BROKER_URL -r job1 -p -b $f
    > done
    ```

    This pushes 8 messages in rabbitmq and the job should now start running and reading them off the queue and spawing new ones as they exit.
