lint:
	docker exec wh-backend ruff check .

test:
	docker exec -it wh-backend pytest .

b-logs:
	docker logs -f wh-backend

rmi-backend:
	docker stop wh-backend && docker rm wh-backend && docker rmi wh-wh-backend

Start:
	docker compose up -d

Stop:
	docker compose stop