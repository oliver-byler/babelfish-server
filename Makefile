#Defaults
SERVER_PORT=8087
IMAGENAME=rover-takehome:latest

.DEFAULT_GOAL := docker-test

docker:
	    @docker build --build-arg babelserver_port=${SERVER_PORT} -t ${IMAGENAME} .

docker-test:
	    @docker run ${IMAGENAME}

docker-run:
	    @test $${DD_APP_KEY?Please set environment variable DD_APP_KEY}
	    @test $${DD_API_KEY?Please set environment variable DD_API_KEY}
	    @test $${DD_HOST?Please set environment variable DD_HOST}
	    @docker run -p ${SERVER_PORT}:${SERVER_PORT} --env DD_APP_KEY=${DD_APP_KEY} --env DD_API_KEY=${DD_API_KEY} --env DD_HOST=${DD_HOST} --entrypoint "python" ${IMAGENAME} babelserver.py

docker-shell:
	    @docker run -it --env DD_API_KEY=${DD_API_KEY} --env DD_APP_KEY=${DD_APP_KEY} --env DD_HOST=${DD_HOST} --entrypoint "/bin/sh" ${IMAGENAME}
