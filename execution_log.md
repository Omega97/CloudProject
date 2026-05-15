
# Execution Log

> This is the log of the part of the project *after* we built the repo of the **cloud-based file storage system**.

---

## Docker Configuration

### 🤖 Run the command prompt in admin mode
```
Win + X -> A
```

### 💥 Activate the virtual environment
```
cd C:\Users\monfalcone\PycharmProjects\CloudProject
.venv\Scripts\activate
```

### 🐳 Run Docker
```
"C:\Program Files\Docker\Docker\Docker Desktop.exe"
```
(or `docker_desktop` if you set up the shortcut)
Wait for Docker to initialize...

#### ✅ Check that Docker is working (optional)
```
docker version
```

### 📦 Startup - build the containers
```
docker compose --env-file .\env\.env up -d --build
```
The `--build` argument is optional, as it forces Docker to rebuild the images before starting the containers.

#### ✅ Check status (optional)
```
docker compose --env-file .\env\.env ps
docker ps -a
```

---

## Nextcloud 


### Features

All of the following features are automatically provided by Nextcloud.

**Admin Capabilities**
- [x] Log in to Nextcloud
- [x] Create new users
- [ ] Delete users
- [ ] Reset user passwords
- [ ] Create, manage, and assign Groups

**Admin File Storage Management**
- [x] Upload, download, delete, rename, move files and folders
- [ ] Create shares (links, with password, expiration date, etc.)
- [ ] Access other users' files (if given permission)

**System Administration**
- [ ] Install/uninstall Nextcloud Apps (Calendar, Contacts, Notes, OnlyOffice, etc.)
- [ ] Configure security settings (password policy, MFA, etc.)
- [ ] View system logs and activity

**Regular User Capabilities**
- [x] Log in to Nextcloud
- [x] **Have their own private storage space** (`/remote.php/dav/files/username/`)
- [x] **Upload files** (via web drag & drop or WebDAV)
- [x] **Download files**
- [x] **Delete files** and folders
- [x] Create folders
- [x] Preview many file types (images, PDFs, text, etc.)
- [ ] Share files/folders with others or via public link

---

#### ✅ Container table (optional)
```
docker compose ps
```

### 🌐 Nextcloud in the Browser 

> Hop on http://localhost:8080 to log into the **admin account**.

You can find your credentias in the `env\.env` file.
```
NEXTCLOUD_ADMIN_USER=[username]
NEXTCLOUD_ADMIN_PASSWORD=[password]
```
You should now be logged into the admin account.

As an admin, you can create new user account from:
`User icon (top right) > Users > New user`

Example:
- omar (omarcf)
- VeryStr0ngPassword.
- omar.cusma.fait@gmail.com

#### Users have their own private storage space 
On Windows (using Docker Desktop with the WSL2 backend), these files are typically stored within the hidden WSL utility distribution at:
`\\wsl$\docker-desktop-data\data\docker\volumes\cloudproject_nextcloud_data\_data\data\<username>\files\`

---

## Monitoring


#### Exporter 🔢

> Visit http://localhost:9205/metrics 

You should be seeing:
```
# HELP go_gc_duration_seconds A summary of the pause duration of garbage collection cycles.
# TYPE go_gc_duration_seconds summary
go_gc_duration_seconds{quantile="0"} 7.5457e-05
...
```

#### Prometheus 🔥 

> Visit http://localhost:9090/targets

The `nextcloud-exporter` should have a status of UP.

You should be seeing:
```
Prometheus  Alerts / Graph / Status /Help
Targets: nextcloud-exporter (1/1 up)
...
```

#### Grafana 🌀

> Visit http://localhost:3000

You can find the admin credentials in the `.env` file.
Since `datasource.yml` is already set up to provision Prometheus, you should be able to start creating a dashboard immediately. 

You should be seeing:
```
Grafana    Home
Welcome to Grafana
Need help? / Documentation / Tutorials / Community / Public Slack / Basic
...
```

#### Locust 🦗

> Visit http://localhost:8089

- Set the Target: Use http://nextcloud as the host.
- Start Swarming: Start with a small number of users (e.g., 5–10) to ensure the `WebDavUser` tasks (upload/download/delete) are executing without errors.

You should be seeing:
```
Locust
Host http://nextcloud
Status: ready
RPS: 0
Failures: 0%

Start new load test
Number of users (peak concurrency): 1
Ramp Up (users started/second): 1
Host: http://nextcloud
...
``` 

---

## Stress Test with Locust

- Number of users (peak concurrency): 30
- Ramp Up (users started/second): 1
- Host: http://nextcloud
- START SWARM

[Results](data/locust_data.txt)

---

## Large File Test



---

#TODOs...
- "The system should be scalable, secure, and cost-efficient"
- Scalability: "How well does the system handle increased load? How does the system perform on  small files (a few KB), large files (GBs), and average (MBs)"
- Security: "Are appropriate security measures implemented?"
- Cost-Efficiency: *"Has the student considered cost implications and optimized the system accordingly?"
- Internal Metrics: Nextcloud Exporter?
- Time-series Database and Monitoring System: Prometheus?
- Data Visualization: Grafana?
- Performance & Load Testing: Locust? 

---

## Shut-down

#### 🛑 To **shut down** Docker
```
docker compose --env-file .\env\.env down
```
(or `docker_down` if you set up the shortcut)
