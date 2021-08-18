# Overview

The goal of this exercise is to write a simple, locally running web service that receives an http POST request from a service called Loggly, representing an alert, and to then create an event in a service called Datadog representing all the information from the Loggly alert.

# Babelfish Server Design

Babelserver is written in python with CherryPy as a boilerplate web framework to translate and replicate metrics/alerts/events between multiple providers.

When running, Babelserver has the primary endpoint `/translate` and a health monitoring endpoint `/health`. It expects a json payload that constitutes the entirety of a providers message and will translate into the correct format for the desired downstream provider. This is currently only built to work with Loggly -> Datadog translation.

## Requirements/Dependencies

docker >= 20.0.0 and make

## Usage

- `make docker` - build a local docker image

- `make docker-run` - run babelserver in foreground listening on port 8087 ( configurable in Makefile )

- `make docker-shell` - run babelserver with interactive sh

- `make docker-test` - run all unit/integration tests. This is the default make target.

*Make sure to your Datadog credentials via environment variables: DD_API_KEY, DD_APP_KEY, DD_HOST

## Example Request

- Exec `make docker-run` to get it running in the foreground
- Create a mocked Loggly Alert payload:

`{"alert_name":"foo","edit_alert_link":"1","source_group":"foo","start_time":"Jan 1 00:00:00","end_time":"Jan 1 00:00:01","search_link":"foobar","query":"foo","num_hits":0,"recent_hits":[],"owner_username":"foo","owner_subdomain":"bar","owner_email":"foo"}`
- Send this payload to the Babelfish Server with your tool of choice:

`curl -d '{"alert_name":"foo","edit_alert_link":"1","source_group":"foo","start_time":"Jan 1 00:00:00","end_time":"Jan 1 00:00:01","search_link":"foobar","query":"foo","num_hits":0,"recent_hits":[],"owner_username":"foo","owner_subdomain":"bar","owner_email":"foo"}' -H "Content-Type: application/json" -X POST http://localhost:8087/translate`
- Observe event created in Datadog event stream: https://app.datadoghq.com/event/stream

![image](https://user-images.githubusercontent.com/12144004/129983875-0c3bdcd8-765b-414f-9d5a-36a1b5a279c5.png)
