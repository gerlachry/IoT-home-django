# IoT-home-django
start postgres via docker locally
	docker run --name auto-db -e POSTGRES_PASSWORD=postgres -d postgres	

start elastic search via docker locally
	docker run -d elasticsearch

list all containers
	docker ps -a

restart postgres
	docker restart auto-db

restart elasticsearch 
	docker restart auto-es
