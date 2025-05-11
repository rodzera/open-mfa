dev-up:
	docker compose --env-file dev/.env -f docker-compose.yaml -f dev/docker-compose.dev.yaml up -d

dev-restart:
	docker compose --env-file dev/.env -f docker-compose.yaml -f dev/docker-compose.dev.yaml restart

dev-down:
	docker compose --env-file dev/.env -f docker-compose.yaml -f dev/docker-compose.dev.yaml down

prd-up:
	docker compose --env-file prd/.env -f docker-compose.yaml -f prd/docker-compose.prd.yaml up -d

prd-restart:
	docker compose --env-file prd/.env -f docker-compose.yaml -f prd/docker-compose.prd.yaml restart

prd-down:
	docker compose --env-file prd/.env -f docker-compose.yaml -f prd/docker-compose.prd.yaml down
