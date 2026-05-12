from locust import HttpUser, task, between
import os, uuid

NC_USER = os.getenv("NC_USER", "admin")  # or set Host as http://admin:PASSWORD@nextcloud

class WebDavUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.dav_root = f"/remote.php/dav/files/{NC_USER}"
        self.name = f"locust-{uuid.uuid4().hex[:8]}.txt"
        self.payload = b"hello from locust\\n"

    @task(2)
    def upload(self):
        with self.client.put(f"{self.dav_root}/{self.name}", data=self.payload, name="webdav PUT", catch_response=True) as r:
            if r.status_code not in (200, 201, 204):
                r.failure(f"PUT failed: {r.status_code}")

    @task(2)
    def download(self):
        self.client.get(f"{self.dav_root}/{self.name}", name="webdav GET")

    @task(1)
    def delete(self):
        self.client.delete(f"{self.dav_root}/{self.name}", name="webdav DELETE")
