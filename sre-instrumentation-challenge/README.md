# SRE Instrumentation Challenge

> Solution attempt by **Daniel Steinmann**. Steps and decisions taken are documented here using Markdown blockquotes (like this one). A detailed, unfiltered worklog is provided in `notes.md`. I planned to also dockerize the traffic generator, but skipped it due to lack of time.
>
> - I made sure to keep track of time very precisely (see `notes.md`)
> - I worked almost exclusively with the official documentation, limiting AI usage to an absolute minimum. I leverage AI in technologies that I am an expert in, but for new tools I prefer to have a deep-dive first.
> - Timetable (Total: 5.5h)
>   - Planning and setup (30m)
>   - Exporter and minimal instrumentation (1h)
>   - Trying integration without dockerization (30m)
>   - Refresh Docker fundamentals (1h)
>   - Write and test dockerfile, add to docker-compose (1h)
>   - Integrate, test and create dashboards (1h)
>   - Extend README and documentation (30m)
>
> **Review instructions**
>
> 1. Run `docker compose up`
> 2. Run `scripts/generate_traffic.sh`
> 3. Refresh dashboards in on Grafana Frontend (http://localhost:3000/)

Your goal is to add Prometheus instrumentation to our in-memory Storage API which is written in Python (see `src/README.md` for more details).

**Please invest no more than 5 to 8 hours.** If you cannot complete the task in this time frame, document where you got stuck so we can use this as a basis for discussion for your next interview.

## Your mission, should you choose to accept it:

### Step 1: Implementation

- Add the Prometheus metrics endpoint to the Storage API
  > - Implemented using https://github.com/prometheus/client_python
  > - Stayed as close as possible to documentation
  > - No Python deep-dive, since I am not a professional Python developer
- Expose HTTP request duration in seconds by path, method and status code
  > - Started out without labels to keep it simple, tested with provided script
  > - Planned implementation improvement of `status_code` label for the very end of the timebox. Using `time.perf_counter()` looks non-canonical to me, I am sure there is a better solution for this, since dynamic labeling must be a ubiquitous use-case.
- Create a Dockerfile for the Storage API. The Prometheus Server expects it to run on `http://storage_api:5000`.
  > - Intended to skip this step at first, but realized that the preconfigured networking setup could then not be used
  > - I have never written Dockerfiles myself, so I spent about an hour refreshing on Docker principles to make sure I could explain what I'm doing
  > - Decided to keep it very simple, but interested to learn more about more advanced concepts like caching, staging and volume setup.
- Add the newly dockerized Storage API to our docker-compose setup
  > - That worked out-of-the-box, and using the Prometheus and Grafana frontends I could verify that the integratoin worked.

### Step 2: Visualization

1. Run `docker-compose up`
2. Create a new Grafana dashboard here: http://localhost:3000
3. The dashboard should contain two graphs for our Storage API:

- Average HTTP Request Duration
- HTTP Status Codes

It should look something like this:

![docs/grafana-dashboard.png](docs/grafana-dashboard.png)

Tip: Run `scripts/generate_traffic.sh` to generate some traffic to the Storage API . The script expects the Storage API to run on http://localhost:5000.

> - Reading up on the Prometheus Query Language, creating the dashboards was straightforward
> - The dashboards could be prettified, which I would do for a production use-case. In this case, I assume that it is not a primary focus.
> - The dashboard provisioning feature is very elegant

4. Try to figure out why you see HTTP 500 errors for some endpoints
   > - For a successful delete, the API should return 204 (or 200) instead of 500

### Step 3: Deployment

> Not having previous experience, implementing the Kubernetes setup would have exceeded the timebox, so I decided to skip this part.

In the last step we want to run the setup we have from our `docker-compose.yml` file on Kubernetes. Please create the Kubernetes resources for

- Storage API application
- Prometheus
- Grafana

How you create or generate the resource files (YAML files) is up to you. Depending on the time left, it is fine to take shortcuts or only creating the resource files without actually applying them to a Kubernetes cluster. Also don't invest much time into the volume setup.

## Evaluation criteria

What we're looking for:

- We expect the resulting Storage API to be equally simple. Even if you don't know Python, the Flask and Prometheus documentation should provide enough guidance
- The Dockerfile and your changes to docker-compose.yml are sensible and concise. You can talk about the pros and cons of your setup in relation to convenience vs security.
- It works reliably. `docker-compose up` and your documentation should be all that is required to review your solution
- Scratch features when necessary, time is short!
- Document your approach, your decisions, and your general notes
