fib
===

This project provides a RESTful web service.
The web service accepts a number, n, as input and returns the first n Fibonacci numbers
The service returns the response as a JSON document

Installation
------------

The application can be installed by cloning the project and running the setup.py script:

    python setup.py install

It can also be installed directory from git using tarball:

    pip install https://github.com/nonameentername/fib/tarball/master#egg=fib

Run
---

Once installed the application can be started with the following command:

    python -m fib.api.app

The service will run on port 8080.
To get a list of the first 5 Fibonacci numbers execute on the terminal:

    curl -X GET http://localhost:8080/5 | python -m json.tool

output:

    [
        0,
        1,
        1,
        2,
        3
    ]

Test
----

The project uses tox to test with different versions of python

To install tox execute the following command:

    pip install tox

And to run the test:

    tox

A code coverage report is generated under htmlcov


Deploy
------

This application uses docker to publish the application.
The docker image is built using ubuntu 14.04 with nginx and uwsgi

To build the docker image run the following command:

    docker build -t fib .

To run the service with docker on port 8080:

    docker run -p 8080:80 fib

An image has been upload to the public docker registory.
This can be run with the following command:

    docker run -p 8080:80 werner/fib

This will download the image and run it on port 8080
