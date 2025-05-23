lint:
	ruff check .

test:
	docker exec -it sc-backend pytest .

b-logs:
	docker logs -f sc-backend

rmi-backend:
	docker stop sc-backend && docker rm sc-backend && docker rmi storagecontrol-sc-backend

Start:
	docker compose up -d

Stop:
	docker compose stop