**Cloud Computing Project Report**  
**Self-Hosted Cloud File Storage System with Nextcloud**  
**Student: Omar Cusma Fait**  
**Course: Cloud Computing Basic**  
**Date: May 2026**

---

### Project Overview

The goal of this project was to design, deploy, and test a **self-hosted cloud-based file storage system**. I chose **Nextcloud** as the core platform because it is a mature, open-source solution that natively supports user management, private storage spaces, WebDAV for file operations, and a rich ecosystem for extensions.

The system was fully containerized using **Docker Compose** and includes a complete observability stack (**Prometheus + Nextcloud Exporter + Grafana**) and load testing with **Locust**. All components run on **Windows 11 with WSL2**.

This setup satisfies the course requirements: user authentication/authorization, file upload/download/delete operations, monitoring, performance testing, and discussion of scalability, security, and cost-efficiency.

---

### Architecture & Implementation

#### Core Components

| Component              | Technology                  | Purpose |
|------------------------|-----------------------------|---------|
| **File Storage**       | Nextcloud 28                | Main application (user files, WebDAV) |
| **Orchestration**      | Docker Compose v3.8         | Multi-container management |
| **Monitoring**         | Prometheus + Nextcloud Exporter | Metrics collection |
| **Visualization**      | Grafana                     | Dashboards and real-time analytics |
| **Load Testing**       | Locust                      | Stress testing (upload/download/delete) |
| **Persistent Storage** | Docker Volumes              | Nextcloud data, Prometheus, Grafana |

**Key Docker Compose services** (see `docker-compose.yml`):
- `nextcloud`: Main app with admin user pre-configured.
- `nextcloud-exporter`: Exposes Nextcloud metrics in Prometheus format.
- `prometheus`: Scrapes metrics every 30s.
- `grafana`: Pre-provisioned with Prometheus datasource.
- `locust`: Runs custom WebDAV tasks.

All inter-container communication uses Docker’s internal network (service names as hostnames).

**Deployment Environment**: Windows 11 + WSL2. Data persists in Docker volumes (`nextcloud_data`, etc.).

---

### Functionality Achieved

**User Management (Admin)**
- Login as admin
- Create users (e.g., user `omar`)
- Each user gets a private storage space at `/remote.php/dav/files/username/`

**File Operations (Regular Users)**
- Upload, download, delete files via WebDAV (tested with Locust)
- Create folders, preview files through the web UI

**Monitoring**
- Nextcloud Exporter → Prometheus → Grafana
- Key metrics visualized: `nextcloud_up`, active users, total files, request rates, scrape duration.

**Load Testing**
- Custom Locust script (`locust-tasks/tasks.py`) performs randomized upload + cleanup with controllable file sizes (50KB–50MB).
- Tasks use proper Basic Auth and random file content (`os.urandom`).

Detailed step-by-step execution guide is available in [`execution_log.md`](execution_log.md).

---

### Results & Challenges

#### Performance Testing (Locust)
I ran multiple stress tests with different file sizes.  
**Example results** (from `data/locust_data.txt` – small files):

- ~15 RPS with 30 users
- Average response time ~15–16 ms
- 100% failure rate on initial runs due to authentication issues (fixed by correct credentials and timeouts)

**Major Challenge**: Running Locust for too long with large files filled up the WSL2 disk. I had to use `diskpart` to shrink/expand the virtual hard disk.  
**Solution implemented**: Added timeouts in Locust tasks and limited test duration. Later versions of `tasks.py` include automatic cleanup after each upload.

#### Monitoring Challenges
- Initially struggled to get Grafana to show Nextcloud metrics.
- **Solution**: Used the official provisioning file (`grafana/provisioning/datasources/datasource.yml`) and correct internal service names (`http://prometheus:9090`). Verified via `http://localhost:9205/metrics`.

#### Other Lessons Learned
- Pinned Docker images with digests for reproducibility.
- Created detailed documentation (`execution_log.md`, README) because I was new to the whole stack.
- Learned the importance of proper authentication, volume management, and resource limits in Docker.

---

### Security Measures

- **Authentication**: Basic Auth over WebDAV + Nextcloud’s built-in user system.
- **Data isolation**: Each user has private storage.
- **Network**: All services run in isolated Docker network; exposed only on localhost.
- **Transport**: Runs over HTTP locally (production recommendation: add Traefik or Nginx with TLS).
- **Best practices followed**: Strong passwords, least-privilege users for Locust, no hardcoded secrets in code (loaded from `.env`).

**Limitations**: No MFA or full encryption at rest configured in this local demo (available in Nextcloud).

---

### Scalability & Cost-Efficiency

**Scalability Discussion**
- **Vertical**: Increase container resources (CPU/memory) and Nextcloud’s PHP-FPM/worker settings.
- **Horizontal**: Deploy multiple Nextcloud instances behind a load balancer + shared storage (e.g., NFS or S3 via MinIO).
- **Storage**: Nextcloud can use object storage backends (S3-compatible) for large scale.
- **Observed behavior**: Small files (50KB) handled efficiently; larger files (20–50MB) increase latency and disk I/O significantly.

**Cost-Efficiency**
- All open-source tools → **zero licensing cost**.
- Lightweight containers and efficient monitoring keep resource usage low.
- Local Docker deployment is ideal for development/testing.
- In production, using spot instances or auto-scaling groups on cloud providers would optimize costs.

---

### Cloud Deployment Plan (Production)

**Recommended Provider**: **AWS**

**Architecture**:
- **EC2** or **ECS/Fargate** for Nextcloud containers
- **S3** (or **EFS**) for file storage
- **RDS PostgreSQL** as database backend (better than SQLite)
- **ElastiCache Redis** for caching
- **ALB + Route 53** + ACM for TLS termination
- **Prometheus + Grafana** on EC2 or use **Amazon Managed Grafana**
- **Auto Scaling Group** based on CPU / request load

**Justification**: AWS offers excellent managed services, pay-as-you-go pricing, strong security (IAM, VPC, Security Groups), and global reach. Alternatives like Azure or GCP are also viable, but I am most familiar with AWS.

---

### Future Improvements

- Add PostgreSQL + Redis for better performance/scalability.
- Implement full CI/CD (GitHub Actions) for Docker images.
- Add alerting via AlertManager + Slack/Email.
- Enable Nextcloud encryption and MFA.
- Deploy behind a reverse proxy with rate limiting.
- Test with real large files (GB range) and optimize storage backend.

---

### Conclusion

This project successfully delivered a functional, monitored, and load-tested self-hosted cloud storage system using Nextcloud and modern DevOps tools. Despite initial challenges with tooling, disk management, and metric integration, the final setup is stable and well-documented.

The exercise reinforced key cloud concepts: containerization, observability, load testing, and the trade-offs between self-hosted and managed services. The system meets all functional requirements and provides a solid foundation for further scaling in the cloud.
