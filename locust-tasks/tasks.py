"""
Locust task v6 - Controlled File Size Testing (Upload & Cleanup)

Choose ONE size by uncommenting the associated task, among:
- test_50kb
- test_500kb
- test_5mb
- ...
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
        print(f"✅ Authenticated as {self.username}")  # This will show in container logs

    def _upload(self, size_bytes: int, label: str):
        filename = f"test_{label}_{uuid.uuid4().hex[:8]}.dat"
        data = os.urandom(size_bytes)

        # Upload
        with self.client.put(f"{self.remote_path}{filename}",
                             data=data,
                             auth=self.auth,
                             catch_response=True,
                             name=f"Upload {label}") as r:
            if r.status_code not in [201, 204]:
                r.failure(f"Upload failed: {r.status_code}")
                return

        # Delete
        with self.client.delete(f"{self.remote_path}{filename}",
                                auth=self.auth,
                                catch_response=True,
                                name=f"Delete {label}") as r:
            if r.status_code == 204:
                r.success()
            else:
                r.failure(f"Delete failed: {r.status_code} - Check permissions")

    # ================== Choose ONE size by uncommenting ==================

    @task(1)
    def test_50kb(self):
        self._upload(50 * 1024, "50kB")

    # @task(1)
    # def test_500kb(self):
    #     self._upload(500 * 1024, "500kB")

    # @task(1)
    # def test_5mb(self):
    #     self._upload(5 * 1024 * 1024, "5MB")

    # @task(1)
    # def test_20mb(self):
    #     self._upload(20 * 1024 * 1024, "20MB")

    # @task(1)
    # def test_50mb(self):
    #     self._upload(50 * 1024 * 1024, "50MB")
