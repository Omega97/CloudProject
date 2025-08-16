PROJECT ?= cloudproject
ENV_FILE ?= env/.env
COMPOSE = docker compose --env-file $(ENV_FILE)

.PHONY: up down stop ps logs logs-% restart clean prometheus grafana locust

up:          ## Start (build + detach)
$(COMPOSE) up -d --build

down:        ## Stop & remove containers (keep volumes)
$(COMPOSE) down

stop:        ## Stop containers only
$(COMPOSE) stop

ps:          ## Show status
$(COMPOSE) ps

logs:        ## Tail all logs
$(COMPOSE) logs -f

logs-%:      ## Tail logs of one service: make logs-nextcloud
$(COMPOSE) logs -f $*

restart:     ## Restart everything
$(COMPOSE) down && $(COMPOSE) up -d

clean:       ## Nuke containers + volumes + local images (⚠️ data loss)
$(COMPOSE) down -v --rmi local

prometheus:  ## Recreate only Prometheus
$(COMPOSE) up -d --no-deps --build prometheus

grafana:     ## Recreate only Grafana
$(COMPOSE) up -d --no-deps --build grafana

locust:      ## Recreate only Locust
$(COMPOSE) up -d --no-deps --build locust
