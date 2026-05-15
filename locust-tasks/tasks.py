"""Locust task v4"""
import uuid
import os
from locust import HttpUser, task, between


class WebDavUser(HttpUser):
    # Wait between 5 and 10 seconds between tasks for large files
    # to avoid overwhelming the network immediately.
    wait_time = between(5, 10)

    # Credentials (Update if changed in UI)
    username = "omar"
    password = "VeryStr0ngPassword."

    def on_start(self):
        self.remote_path = f"/remote.php/dav/files/{self.username}/"
        self.auth = (self.username, self.password)

    def _perform_upload(self, size_bytes, label):
        filename = f"loadtest_{label}_{uuid.uuid4().hex}.dat"
        # Generate random incompressible data
        data = os.urandom(size_bytes)

        with self.client.put(
                f"{self.remote_path}{filename}",
                data=data,
                auth=self.auth,
                catch_response=True,
                name=f"Upload {label}"
        ) as response:
            if response.status_code in [201, 204]:
                response.success()
                return filename
            else:
                response.failure(f"{label} upload failed: {response.status_code}")
                return None

    @task(10)
    def test_small_file(self):
        """Simulates tiny documents or metadata (10 KB)"""
        self._perform_upload(10 * 1024, "10KB")

    @task(3)
    def test_medium_file(self):
        """Simulates average photos or PDFs (5 MB)"""
        self._perform_upload(5 * 1024 * 1024, "5MB")

    @task(1)
    def test_large_file(self):
        """Simulates high-resolution video or archives (50 MB)"""
        # Note: 50MB is a good stress point for a local docker setup.
        # If your machine is very fast, try 100MB.
        self._perform_upload(50 * 1024 * 1024, "50MB")

    @task(2)
    def download_and_cleanup(self):
        """Cleanup task to keep the container storage from filling up"""
        # List files first (optional) or just move on
        pass
