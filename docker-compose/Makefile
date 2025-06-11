dev-up:
	docker compose --env-file dev/.env -f docker-compose.yaml -f dev/docker-compose.dev.yaml up -d

dev-restart:
	docker compose --env-file dev/.env -f docker-compose.yaml -f dev/docker-compose.dev.yaml restart

dev-down:
	docker compose --env-file dev/.env -f docker-compose.yaml -f dev/docker-compose.dev.yaml down

staging-up:
	docker compose --env-file staging/.env -f docker-compose.yaml -f staging/docker-compose.staging.yaml up -d

staging-restart:
	docker compose --env-file staging/.env -f docker-compose.yaml -f staging/docker-compose.staging.yaml restart

staging-down:
	docker compose --env-file staging/.env -f docker-compose.yaml -f staging/docker-compose.staging.yaml down
