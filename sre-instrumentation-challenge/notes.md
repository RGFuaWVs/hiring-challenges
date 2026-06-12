# Notes SRE Challenge

Starting Time: 20:39

# Get started

1. Fork repo (https://github.com/axpogroup/hiring-challenges/tree/main/sre-instrumentation-challenge), checkout
2. Read instructions

# Planning

1. Set up python environment
2. Run storage api locally
   1. Test with provided script
   2. Check why HTTP 500s occur (probably no instrumentation required yet)
3. Prometheus
   1. Check documentation for Python API instrumentation
   2. Add instrumentation to app
      1. Request duration in seconds. Dimensions:
      - Path
      - Method (I suppose HTTP method)
      - Status Code
      1. Labels from example image:
         1. Average HTTP Request Duration - Value
         2. HTTP Status Codes - 200, 404, 500
   3. Test instrumentation
4. Dockerfile (maybe skip, no experience)
   1. Check documentation for dockerfile for python app
   2. Create dockerfile (run on correct path)
   3. Add to docker compose
5. Grafana Dashboard
   1. Checkout localhost:3000 to see what's happening
   2. If Dockerfile could not be created, run Python app locally
6. Kubernetes (probably skip, no experience)
7. Run test script again and check if dashboard works
8. Add documentation if necessary

Time: 20:55

## Final URIs

Storage API: http://localhost:5000 (maybe there is an error in the README, http://storage_api:5000 does not look like a valid local URI)
Grafana Dashboard: http://localhost:3000

# Execution

## Set up Python environment

- Set up .venv in VS Code with Python 3.14.0
- Get development setup to work
- Make does not seem to work on windows, install via chocolatey
- Probably was inteded for MacOS or Linux, but I don't want to switch now, so let's see if this works with little effort
- YES it seems to work, so let's stay on Windows for now
- Run tests: Success!
- Run service: Success, service runs on port 5000

## Test API with provided script

- Script runs, but does not output logs, let's check it out
- Adding an echo to the script: Success, can see output
- Better: remove --silent flag
- Get error: Couldn't connect to server
- Localhost is usually 127.0.0.0, let's change that in the run.py for a quick test
- Ok something is wrong here, let's use the curls from the README to test the api
- Quick research: 0.0.0.0 refers to no particular address, so it should work with localhost
- Try with postman: SUCCESS with localhost:5000

TIME: 21:15

- Ah, bash script automatically ran on WSL, probably caused connectivity error
- Ok, let's do everything in WSL, probably easier than on windows.
  1. Commit, clone again in WSL
- Ok, we're back, that was quick. Let's see if make works natively now
- First install VSCode python extensions again
- Failed to create venv, do it manually
- Ok, getting there, run make again: Success!
- Yes test script seems to work, check the curls
- Curls work, too
- Ok, now let's see about the 500s
  - Successful delete should return 204 No Content, returns 500 now. Let's not change it though so we can see it on the dashboard, too.

TIME: 21:27

## Prometheus

- Know +/- how it works but never worked with, so let's take 10 minutes to skim documentation for Python implementations
- Found https://github.com/prometheus/client_python, let's read
  - We'll have to add package "prometheus-client"
  - Quickstart uses decorator. Probably not enough if we need to use status code dimensions
  - Instrumenting
    - We don't need quantiles, so "Summary" should do
    - "request_latency_seconds" looks good (https://prometheus.github.io/client_python/instrumenting/summary/)
    - Let's see what "Labels" are
      - https://prometheus.github.io/client_python/instrumenting/labels/
      - Grouping, exactly what we want
      - Labels should be added with c.labels(..), example `c.labels('/buckets/<id>', 'GET', 200)
        [ ] Have to interpolate path and status code
    - "Real-world example" looks good, probably copy that
    - But do i need to start a http server? I already have one, right?
  - Exporting
    - We are using "flask", so https://prometheus.github.io/client_python/exporting/http/flask/ seems to be all that's needed

### TODO

TIME: 21:38

[ ] Add exporter
[ ] Add instrumentation
[ ] Check metrics endpoint when test script runs
