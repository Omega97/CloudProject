# Presentation Slides for CloudProject

---

## **Slide 1: Project Overview**

**Cloud-Based File Storage System**
*Cloud Computing Basic Course - May 2026*

**Objective:**
Deploy a self-hosted cloud storage platform with monitoring and performance testing capabilities

**Key Components:**
- **Nextcloud**: File storage and user management
- **Docker Compose**: Container orchestration
- **Prometheus + Grafana**: Monitoring and visualization
- **Locust**: Load testing and performance analysis

**Requirements Addressed:**
✓ User authentication & authorization  
✓ Private storage spaces  
✓ File operations (upload/download/delete)  
✓ Scalability, security, and cost-efficiency  

**[INSERT: Project architecture diagram or Nextcloud logo]**

---

## **Slide 2: System Architecture**

**Multi-Container Docker Environment**

| Component          | Port | Purpose                 |
|--------------------|------|-------------------------|
| Nextcloud          | 8080 | Main application        |
| Nextcloud Exporter | 9205 | Metrics exposure        |
| Prometheus         | 9090 | Time-series database    |
| Grafana            | 3000 | Visualization dashboard |
| Locust             | 8089 | Load testing            |

**Data Flow:**
1. Nextcloud → Exporter → Prometheus → Grafana
2. Locust → WebDAV API → Nextcloud

**[INSERT: Docker Compose architecture diagram showing container connections]**

---

## **Slide 3: Docker Setup & Configuration**

**Environment: Windows 11 + WSL2**

**Startup Process:**
```bash
# Activate environment & start Docker
.\.venv\Scripts\activate
"C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Launch the complete stack
docker compose --env-file .\env\.env up -d --build

# Verify containers
docker compose ps
```

**Key Configuration:**
- **Image pinning** with SHA256 digests for reproducibility
- **Persistent volumes**: nextcloud_data, prometheus_data, grafana_data
- **Network**: Internal Docker network for service communication
- **Environment variables**: Credentials and settings in `.env` file

**[INSERT: Screenshot of docker compose ps output or terminal]**

---

## **Slide 4: Nextcloud Features**

**Admin Capabilities:**
- ✓ User account creation and management
- ✓ Private storage allocation per user (`/remote.php/dav/files/username/`)
- ✓ Group management and permissions
- ✓ System configuration and security settings

**User Capabilities:**
- ✓ Upload/download/delete files via WebDAV
- ✓ File preview (images, PDFs, text)
- ✓ Folder creation and organization
- ✓ Web interface and desktop sync

**WebDAV Endpoint:**
```
/remote.php/dav/files/{username}/
```

**[INSERT: Screenshot of Nextcloud web interface showing file browser]**

---

## **Slide 5: Monitoring Stack**

**Metrics Collection Pipeline:**

**1. Nextcloud Exporter**
- Scrapes Nextcloud internal metrics
- Exposes data at `http://localhost:9205/metrics`
- Key metrics: active users, file count, response times

**2. Prometheus**
- Time-series database
- Scrape interval: 15-30 seconds
- Configuration: `prometheus/prometheus.yml`

**3. Grafana**
- Auto-provisioned Prometheus datasource
- Custom dashboards for real-time monitoring
- Access: `http://localhost:3000`

**[INSERT: Screenshot of Grafana dashboard or Prometheus targets page]**

---

## **Slide 6: Load Testing with Locust**

**Testing Framework: Locust**

**Test Configuration:**
- **Script**: `locust-tasks/tasks.py`
- **User simulation**: WebDavUser class
- **Authentication**: Basic Auth (username/password)
- **Wait time**: 1-3 seconds between tasks

**Test Tasks:**
```python
@task(2)  # 40% weight
def upload(self):    # PUT request
    
@task(2)  # 40% weight
def download(self):  # GET request
    
@task(1)  # 20% weight
def delete(self):    # DELETE request
```

**Access**: `http://localhost:8089`

**[INSERT: Screenshot of Locust web interface]**

---

## **Slide 7: Test Execution**

**Test Parameters:**
- **Duration**: ~1 minute (09:00:02 - 09:01:14)
- **Target Host**: `http://nextcloud`
- **File sizes**: 50KB - 50MB (configurable)
- **Random content**: `os.urandom()` for incompressible data

**Test Workflow:**
1. Generate unique filename with UUID
2. Create random binary data
3. Upload file via WebDAV PUT
4. Download file via WebDAV GET
5. Delete file via WebDAV DELETE
6. Cleanup to prevent disk overflow

**Challenge Encountered:**
- Initial 401 Unauthorized errors
- Solution: Proper authentication credentials and timeout configuration

**[INSERT: Locust task distribution pie chart or workflow diagram]**

---

## **Slide 8: Performance Statistics**

**Test Results Summary:**

| Metric                    | Value      |
|---------------------------|------------|
| **Total Requests**        | 864        |
| **Test Duration**         | 72 seconds |
| **Average Response Time** | 15.69 ms   |
| **Median Response Time**  | 15 ms      |

**Request Breakdown:**

| Operation          | Requests | Median (ms) | Avg (ms) | Min/Max (ms) |
|--------------------|----------|-------------|----------|--------------|
| **PUT (Upload)**   | 331      | 15          | 15.41    | 9 / 30       |
| **GET (Download)** | 351      | 15          | 15.79    | 9 / 29       |
| **DELETE**         | 182      | 15          | 16.00    | 9 / 85       |

**Current RPS**: ~15 requests/second

**[INSERT: Bar chart showing request distribution or response time graph from Locust]**

---

## **Slide 9: Challenges & Solutions**

**Key Challenges:**

1. **Authentication Failures (401 Errors)**
   - Problem: All 864 requests failed with Unauthorized
   - Root cause: Incorrect credentials or WebDAV configuration
   - Solution: Verified user credentials and Basic Auth implementation

2. **Disk Space Management**
   - Problem: WSL2 virtual disk filled up during large file tests
   - Solution: Implemented automatic cleanup after upload; used `diskpart` to expand VHD

3. **Monitoring Integration**
   - Problem: Grafana not showing Nextcloud metrics initially
   - Solution: Auto-provisioning via `datasource.yml`; correct service names

4. **Resource Optimization**
   - Added timeouts and wait times between tasks
   - Limited test duration to prevent resource exhaustion

**[INSERT: Grafana metrics graph or error rate chart]**

---

## **Slide 10: Conclusions**

**Achievements:**
✓ Fully containerized Nextcloud deployment  
✓ Complete monitoring stack (Prometheus + Grafana)  
✓ Automated load testing with Locust  
✓ Comprehensive documentation and execution logs  

**Performance Insights:**
- Small files (50KB) handled efficiently (~15ms response)
- System scales well for moderate concurrent load
- Authentication is critical for WebDAV operations

**Future Improvements:**
1. **Security**: Add TLS/SSL via reverse proxy (Traefik/Nginx)
2. **Scalability**: PostgreSQL + Redis backend; horizontal scaling
3. **Cloud Deployment**: AWS EC2 + S3 with auto-scaling
4. **Enhanced Monitoring**: AlertManager integration
5. **Larger Scale Tests**: GB-sized files and 100+ concurrent users

**Cost-Efficiency:**
- All open-source components (zero licensing)
- Lightweight containers optimize resource usage
- Cloud deployment would use spot instances for cost optimization

**[INSERT: Final dashboard screenshot or system performance summary graph]**

---

**Notes for Presentation:**
- Practice timing: ~1 minute per slide
- Be ready to explain Docker networking and volume persistence
- Prepare to discuss the 401 errors and how you'd fix them in production
- Have Grafana dashboard ready for live demo if possible
