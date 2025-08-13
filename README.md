# CloudProject
Cloud-Based File Storage System

---


Render with substitutions; verify new trusted domains appear
```
docker compose --env-file .\env\.env config | Select-String NEXTCLOUD_TRUSTED_DOMAINS
NEXTCLOUD_TRUSTED_DOMAINS: localhost 127.0.0.1 nextcloud
```

Optional: confirm Locust binding is correct in the render
```
docker compose --env-file .\env\.env config | Select-String -Pattern 'locust|/locust-tasks/tasks.py'

  locust:
      - /locust-tasks/tasks.py
    container_name: locust
    image: locustio/locust
        source: C:\Users\monfalcone\PycharmProjects\CloudProject\locust-tasks
        target: /locust-tasks
```

Run the stack 
```
docker compose --env-file .\env\.env up -d --build
error during connect: this error may indicate that the docker daemon is not running: Get "http://%2F%2F.%2Fpipe%2Fdocker_engine/v1.24/containers/json?all=1&filters=%7B%22label%22%3A%7B%22com.docker.compose.config-hash%22%3Atrue%2C%22com.docker.compose.project%3Dcloudproject%22%3Atrue%7D%7D": open //./pipe/docker_engine: The system cannot find the file specified.
```

```
Get-Service com.docker.service
Status   Name               DisplayName                           
------   ----               -----------                           
Stopped  com.docker.service Docker Desktop Service                
```

```
sc.exe query com.docker.service
NOME_SERVIZIO: com.docker.service 
        TIPO                    : 10  WIN32_OWN_PROCESS  
        STATO                   : 1  STOPPED 
        CODICE_USCITA_WIN32     : 1077  (0x435)
        CODICE_USCITA_SERVIZIO  : 0  (0x0)
        PUNTO_CONTROLLO         : 0x0
        SUGGERIMENTO_ATTESA     : 0x0
```

```
sc.exe start com.docker.service
[SC] StartService: OpenService OPERAZIONI NON RIUSCITE 5:

Accesso negato.
```

