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
      - Status Code (TODO)
      1. Labels from example image:
         1. Average HTTP Request Duration - Value
         2. HTTP Status Codes - 200, 404, 500
   3. Test instrumentation
4. Dockerfile (maybe skip, no experience)
   1. Check documentation for dockerfile for python app
   2. Create dockerfile (run on correct path) [TODO: Use separate builder/runner image]
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

added:
Storage API Metrics: http://localhost:5000/metrics
Prometheus Server: http://localhost:9090

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

[x] Add exporter

- First add package, version pinning is always good
- Add exporter and run, http://localhost:5000/metrics already available, YESS

[ ] Add instrumentation

- Okay, start small, let's instrument only the PUT endpoint, copy from docu example, no lables yet
- Hmm, i just put the "with" at the topmost position in the method, but i don't know whether that actually captures e2e latency. Also, how should i group by status code later?
- Ok, nothing seems to be exported yet.
- Ah, i should have set label names, there was an error i did not see
- Continuing tomorrow

TIME: 21:49

TIME: 10:02

- Continuing, working on train from Zurich to Cologne now
- Try instrumentation using decorator as in minimal example
- Type is there, but count and sum are 0
- Let's check prometheus docu to see how i have to query the endpoint
- Counter does not increment, something is still wrong
- Browser caching was the problem. will now check metrics using CURL, too

- Now let's implement it the way we originally wanted.
- Using just one label for now

- Great, now drop the annotation and do it like in the documented "real-world-example"
- Cool, that works, too. Now let's add the other lables to the Get-Endpoint
- How can i add different labels for different paths of the code? Let's just try something
- Trying to find out how exactly .time() works to ensure that I am measuring the right thing
- Ask ChatGPT how to apply label for different status codes. Internet too slow

- Let's skip the status code for now, add remaining labels and continue

TIME: 10:36

- Sanity check on metrics endpoint looks good, commit and continue. Figure out how to add status code when better internet available

## Grafana

- Skipping dockerization of storage API for now, try to spin up existing services in docker-compose.yml and integrate them with locally run storage api
- Internet very slow at pulling images, but at least i'm still in Switzerland
- Moving from WifiOnICE to 5G Hotspot

- Ok seems like we're up, let's check if we can see something in the browser
- Good, grafana runs, i can log in and change the admin password (although then it probably won't work on the next startup)
- Ok, so the port of the storage api, containerized or not, is 5000. I should be able to check whether the prometheus server could has discovered the API.
- Let's first check the prometheus server on 9090
- On "targets" tab it says that the storage api is down. So it should in fact run under http://storage_api:5000, that was no error. I'll change the scrape config and change it back if i can get the dockerfile to work.
- Ok, if i wanted to do it locally, i'd have to add a DNS resolver entry. I'll try that once, if it does not work i'll start working on the dockerfile.
- Ok, that does not work out of the box. Revert the DNS resolver entry, and get started on the dockerfile

## Dockerfile

TIME: 11:05

- Again, let's take 10 minutes to read documentation about how to containerize a python application (https://docs.docker.com/guides/python/containerize/)
- Okay, let's just do it exactly as the docs say
- Create files. Add redundant requirements.txt so that i don't have to change the dockerfile
- So docker compose works, but the app cannot be reached on localhost:8000.
- I think I got something wrong with the networking setup.

- Take a break, check how much time remains, and plan what to do.
  TIME: 11:24
- So far, I've spent 1h + 1.5h = 2.5h on the task. The instrumentation part is ok, and I can probably complete it. Docker is harder, because I have used it a lot, but never actually had to create Dockerfiles. But as soon as the services are up, it should be easy to hook up Grafana and create a Dashboard and have something to show
- I think it would make sense to spend at least 1.5h on Docker fundamentals to be able to debug here. I will take a break, grab a coffee, and then look for a Docker setup with a Python application that I can run and compare to the challenge here.

## Docker Fundamentals

TIME: 11:48

- Let's spend at max until 14h to learn more. (https://docs.docker.com/get-started/)

Priorities:

1. Docker Compose (https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-docker-compose/)
2. Building Images

### Building Images

- Writing a dockerfile (https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/)

- Commands
  - COPY host-path image-path
  - RUN (run something in the container)
  - ENV: Sets environment variable the container will use
  - EXPOSE: Expose a port
  - CMD: Default command container using this image will run (maybe startup app?)

- Best practices (https://docs.docker.com/build/building/best-practices/)

### Multi-stage builds

- Stages (could be leveraged here for dev and prod!)
- "--from" can be used to copy between stages. Looks a bit like azure pipelines and build agents. So this means i can build (or make) the app in one image, and copy the artifacts and run it in another, lighter image. Cool!

### Running containers

- HOST_PORT:CONTAINER_PORT (like reading, from left to right)
- Here I'll probably need more detail, because that is why it didn't work before (https://docs.docker.com/engine/network/#published-ports)
- Overriding container defaults
- Multi-container applications (https://docs.docker.com/get-started/docker-concepts/running-containers/multi-container-applications/)

Okay, i think i got an overview and can now start containerizing the storage API

TIME: 12:19

## Dockerfile 2nd attempt

TIME: 13:23

TIME: 13:53

- Ok, first version that works!
- Now let's expose it on another port
- Commands
  - docker build -t storage_api:latest .
  - docker run -p 8000:5000 storage_api:latest

- Let's improve the image now. I think host and port are not required in CMD, there are defaults in the code
- No, let's improve the image later, now i want to put it together and integrate!

- So theoretically, all that is needed now is to add my image to docker compose and spin it all up
- Yayers, that seems to work now. Now i'll need to figure out how to change the host name
