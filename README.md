# CloudProject
Cloud-Based File Storage System

---

A fully containerized **Nextcloud monitoring and testing stack** built with **Docker Compose**.  
The system integrates **Nextcloud**, **Prometheus**, **Grafana**, and **Locust**, providing a complete environment for **cloud application performance analysis**, **metric collection**, and **real-time visualization**.

Check out the professor's [requirements](https://github.com/Foundations-of-HPC/Cloud-Basic-2023/blob/main/Assignments/Exercise.md).

---

## Exercise for the course Cloud Computing Basic

This is the exercise for Prof. Taffoni and Ruggero of the 2023/2024 Cloud Computing course.

---[.gitkeep](data/.gitkeep)

### Rules

- Materials (code/scripts/pictures and final report) should be prepared on a **GitHub repository**, and **sharing it with the teachers**.
- A **report should be sent by e-mail to the teachers at least five days in advance**: the name of the file should `YOURSURNAME_report.pdf`
- Results and numbers of the exercises should be presented (also with the help of **slides** in a maximum 10-minute presentation: this will be part of the exam). A few more questions on the topic of the courses will be asked at the end of the presentation.

The report should clearly explain **which software stack we should use to deploy** the developed infrastructure and run all the programs you used in your exercises. Providing well-done Makefiles/Dockerfiles/scripts to automatize the work is highly appreciated.

---

### Requirements

*This section explains what you need to do to pass the Cloud Computing part of the exam.*

The exam consists of:

1) Exercise Cloud Computing ([Omega97/CloudProject](https://github.com/Omega97/CloudProject))
2) Documentation (report on GitHub)
3) Presentation of the exercise (ppt)

The deployed platform should be able to:

Manage User Authentication and Authorization:
- Users should be able to sign up, log in, and log out.
- Users should have different roles (e.g., regular user and admin).
- Regular users should have their private storage space.
- Admins should have the ability to manage users.

Manage File Operations:
- Users should be able to upload files to their private storage.
- Users should be able to download files from their private storage.
- Users should be able to delete files from their private storage.

Address Scalability:
- Design the system to handle a growing number of users and files.
- Discuss theoretically how you would handle increased load and traffic.

Address Security:
- Implement secure file storage and transmission.
- Discuss how you would secure user authentication.
- Discuss measures to prevent unauthorized access.

Discuss Cost-Efficiency:
- Consider the cost implications of your design.
- Discuss how you would optimize the system for cost efficiency.

Deployment:
- Provide a deployment plan for your system in a containerized environment on your laptop based on docker and docker-compose.
- Discuss how you would monitor and manage the deployed system.
- Choose a cloud provider that could be used to deploy the system in production and justify your choice.

Test your infrastructure:
- Consider the performance of your system in terms of load and IO operations

---

### The exercise: Cloud-Based File Storage System

You are tasked with identifying, deploying, and implementing a cloud-based file storage system. 
The system should allow users to upload, download, and delete files. 
Each user should have a private storage space. 
The system should be scalable, secure, and cost-efficient. 
Suggested solutions to use for the exam are *NextCloud* and *MinIO*.

---

### Submission details

Documentation:
- The report should explain your choices and describing the platform's architecture, including components, databases, and their interactions.
- Include a section on the security measures taken.

Code:
- Submit the Docker files and any code eventually developed/modified for your cloud-based file storage system.
- Include a README file with instructions on how to deploy and use your system.

Presentation:
- Prepare a short presentation summarizing your design, implementation, and any interesting challenges you faced.
- Be ready to answer questions about your design choices and on the topics discussed during the Cloud Course Lectures

---

### Evaluation Criteria

- Design Clarity: Is the system design well-documented and clear?
- Functionality: Does the system meet the specified requirements?
- Scalability: How well does the system handle increased load? How does the system perform on  small files (a few KB), large files (GBs), and average (MBs)
- Security: Are appropriate security measures implemented?
- Cost-Efficiency: *"Has the student considered cost implications and optimized the system accordingly?"*

---

# 🧭 Project Goals & Progress

---

### ✅ Completed Milestones

* [x] Deploy **Nextcloud** as a self-hosted cloud storage service with user authentication and file operations.
* [x] Set up **Docker Compose** orchestration for multi-service integration.
* [x] Configure persistent storage volumes for Prometheus, Grafana, and Nextcloud.
* [x] Implement **Prometheus monitoring** and **Nextcloud Exporter** for live metrics.
* [x] Auto-provision **Grafana** with Prometheus as the default datasource.
* [x] Run and verify **Locust WebDAV load tests** on the Nextcloud instance.
* [x] Confirm Prometheus metric scraping (`nextcloud_up` = 1).
* [x] Verify Grafana visualizations for Prometheus data.
* [x] Pin all container images by digest for **reproducible builds**.
* [x] Add `.env` and `.env.example` for environment variable management.
* [x] Add Makefile for convenience commands and reproducible execution.
* [x] Document full startup procedure and environment setup.
* [x] Resolve Nextcloud upgrade loop by pinning to v28 (data-compatible).

### 🚧 In Progress / Remaining

* [ ] Create and save **Grafana dashboard** (`nextcloud_overview.json`) summarizing system metrics.
* [ ] Add automatic **Grafana dashboard provisioning** on startup.
* [ ] Collect **Locust load testing results** and visualize them in Grafana.
* [ ] Expand documentation with **security**, **scalability**, and **cost-efficiency** analysis.
* [ ] Write and compile **final report (`report/main.tex`)** explaining architecture, results, and design rationale.
* [ ] (Optional) Deploy on a **remote VM / Cloud provider** for scalability and cost-performance discussion.

---

## ⚙️ Architecture Overview

| Component           | Purpose                                                                                   |
|---------------------|-------------------------------------------------------------------------------------------|
| **Docker Compose**  | Orchestrates all containers and networking.                                               |
| **Nextcloud**       | Simulates a self-hosted cloud storage service under test.                                 |
| **Prometheus**      | Scrapes and stores metrics from Nextcloud Exporter.                                       |
| **Nextcloud Exporter** | Exposes metrics in Prometheus format for scraping.                                    |
| **Grafana**         | Visualizes performance metrics and dashboards.                                            |
| **Locust**          | Generates synthetic load (file uploads/downloads) to stress-test Nextcloud.               |

---

## 🚀 How to Run the Project

---

### 🧰 Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running  
- [Git](https://git-scm.com/)  
- [Python 3.10+](https://www.python.org/downloads/) (for Locust task editing)

---

### 🧩 Setup Steps

```powershell
# Clone the repository
git clone https://github.com/<your-username>/CloudProject.git
cd CloudProject

# Start PowerShell as Administrator
Win + X → “Windows PowerShell (Admin)”

# Activate virtual environment (optional)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\.venv\Scripts\activate

# Start Docker Engine
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Check compose file status
docker compose --env-file .\env\.env ps
```

---

### ▶️ Launch the Stack

```powershell
# Build and start all services
docker compose --env-file .\env\.env up -d
```

| Service                        | URL                                                            | Description              |
| ------------------------------ | -------------------------------------------------------------- | ------------------------ |
| **Nextcloud**                  | [http://localhost:8080](http://localhost:8080)                 | Cloud storage web app    |
| **Prometheus**                 | [http://localhost:9090](http://localhost:9090)                 | Metrics database         |
| **Grafana**                    | [http://localhost:3000](http://localhost:3000)                 | Visualization dashboards |
| **Locust**                     | [http://localhost:8089](http://localhost:8089)                 | Load testing UI          |
| **Nextcloud Exporter Metrics** | [http://localhost:9205/metrics](http://localhost:9205/metrics) | Raw Prometheus metrics   |

---

### 🧪 Running a Load Test

1. Open http://localhost:8089.
2. Set:
   - Number of users: e.g. 10 
   - Spawn rate: e.g. 2 
   - Host: http://nextcloud
3. Click Start Swarming.
4. Observe metrics in Grafana and Prometheus.

---

### 🧹 Shut Down the Stack

```powershell
docker compose down
```

To remove all persisted data:

```powershell
docker compose down -v
```

---

### 🧠 Notes

- Admin credentials (from .env):
  - Nextcloud → admin / <password>
  - Grafana → admin / <password>
- Data and dashboards persist between runs via Docker volumes.
- For dashboard auto-provisioning, create grafana/dashboards/nextcloud_overview.json.
