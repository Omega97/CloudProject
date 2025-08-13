"""
We’re using Locust here because it’s a lightweight, Python-based load testing and benchmarking tool.
- **Purpose** – It simulates multiple concurrent users interacting with the
    Nextcloud instance (uploading, downloading, browsing, etc.) so we can see
    how the system performs under load.
- **Integration** – Because Locust runs inside the same Docker network as
    Nextcloud, it can stress-test the service directly (`http://nextcloud`) without
    worrying about external network delays.
- **Metrics** – It collects response times, request rates, and failure counts,
    which Prometheus and Grafana can visualize in real-time.
- **Why here** – Combined with Prometheus + Grafana, Locust forms the
    “traffic generator” in the monitoring setup, letting evaluate scaling,
    bottlenecks, and error handling in a reproducible way.
"""
from locust import HttpUser, task, between


class NextcloudUser(HttpUser):
    """
    This is enough to verify the plumbing (service DNS, ports, basic responses).
    The compose mounts ./locust-tasks and runs -f /locust-tasks/tasks.py, so this file will be found.

    The @task decorator marks a User class method as a load-testing action that Locust schedules and runs.
    """
    wait_time = between(1, 3)   # small think time

    @task
    def status_and_home(self):
        # Nextcloud status endpoint (unauthenticated JSON)
        self.client.get("/status.php", name="status")
        # Front page
        self.client.get("/", name="home")
