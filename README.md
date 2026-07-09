
# Cloud Project ☁️

Cloud-Based File Storage System

> Check out the [professor's official repo](https://github.com/Foundations-of-HPC/Cloud-Basic-2023/blob/main/Assignments/Exercise.md), and the [execution log](execution_log.md) to see my work! 

- Report: [OCUSMAFAIT_report_Cloud.pdf](report%20&%20slides/OCUSMAFAIT_report_Cloud.pdf)
- Slides: [OCUSMAFAIT_presentation_Cloud.pdf](report%20&%20slides/OCUSMAFAIT_presentation_Cloud.pdf)

---

## ⚙️ Architecture Overview

| Component              | Purpose                                                                                 |
|------------------------|-----------------------------------------------------------------------------------------|
| **Docker Compose**     | Orchestrates all containers and networking.                                             |
| **Nextcloud**          | Simulates a self-hosted cloud storage service under test.                               |
| **Prometheus**         | Scrapes and stores metrics from Nextcloud Exporter.                                     |
| **Nextcloud Exporter** | Exposes metrics in Prometheus format for scraping.                                      |
| **Grafana**            | Visualizes performance metrics and dashboards.                                          |
| **Locust**             | Generates synthetic load (file uploads/downloads) to stress-test Nextcloud.             |

---

## 🚀 How to Run the Project


### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running  
- [Git](https://git-scm.com/)  
- [Python 3.10+](https://www.python.org/downloads/) (for Locust task editing)

---

### Setup Steps 🧩

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

### Launch the Stack ▶️

```powershell
# Build and start all services
docker compose --env-file .\env\.env up -d
```

| Service                        | URL                                  | Description              |
| ------------------------------ |------------------------------------- | ------------------------ |
| **Nextcloud**                  | [http://localhost:8080](http://localhost:8080)         | Cloud storage web app    |
| **Prometheus**                 | [http://localhost:9090](http://localhost:9090)         | Metrics database         |
| **Grafana**                    | [http://localhost:3000](http://localhost:3000)         | Visualization dashboards |
| **Locust**                     | [http://localhost:8089](http://localhost:8089)         | Load testing UI          |
| **Nextcloud Exporter Metrics** | [http://localhost:9205/metrics](http://localhost:9205/metrics) | Raw Prometheus metrics   |

---

### Running a Load Test 🧪

1. Open http://localhost:8089.
2. Set:
   - Number of users: e.g. 10 
   - Spawn rate: e.g. 2 
   - Host: http://nextcloud
3. Click Start Swarming.
4. Observe metrics in Grafana and Prometheus.

---

### Shut Down the Stack 🧹

To shut down Docker, run the command:
```powershell
docker compose down
```

To remove all persisted data:
```powershell
docker compose down -v
```

---
