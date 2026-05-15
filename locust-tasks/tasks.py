"""
Locust task v5 - Controlled File Size Testing

Choose ONE size by uncommenting the associated task, among:
- test_50kb
- test_500kb
- test_5mb
- test_50mb
"""
import uuid
import os
from locust import HttpUser, task, between


class WebDavUser(HttpUser):
    wait_time = between(2, 5)  # Give some breathing room

    username = "omar"
    password = "VeryStr0ngPassword."

    def on_start(self):
        self.remote_path = f"/remote.php/dav/files/{self.username}/"
        self.auth = (self.username, self.password)

    # ================== Choose ONE size by uncommenting ==================

    # @task(1)
    # def test_50kb(self):
    #     self._upload(50 * 1024, "50kB")

    @task(1)
    def test_500kb(self):
        self._upload(500 * 1024, "500kB")

    # @task(1)
    # def test_5mb(self):
    #     self._upload(5 * 1024 * 1024, "5MB")

    # @task(1)
    # def test_50mb(self):
    #     self._upload(50 * 1024 * 1024, "50MB")

    def _upload(self, size_bytes, label):
        filename = f"test_{label}_{uuid.uuid4().hex[:8]}.dat"
        data = os.urandom(size_bytes)

        with self.client.put(
                f"{self.remote_path}{filename}",
                data=data,
                auth=self.auth,
                catch_response=True,
                name=f"Upload {label}"
        ) as resp:
            if resp.status_code in [201, 204]:
                resp.success()
            else:
                resp.failure(f"{label} failed: {resp.status_code}")
