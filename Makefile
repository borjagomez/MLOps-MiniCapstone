
build:
	pip freeze > requirements.txt
	docker build . -t borjagomez/minicapstone

run:
	docker-compose up -d --build
	docker-compose logs -f --tail=20

stop:
	docker-compose down

bash:
	docker run -it borjagomez/minicapstone /bin/bash

logs:
	docker-compose logs -f minicapstone

deploy:
	time=$$(date +'%Y%m%d-%H%M%S') && \
	docker tag borjagomez/minicapstone us-east1-docker.pkg.dev/mlops-3/minicapstoneborja/minicapstone:$$time && \
	docker push us-east1-docker.pkg.dev/mlops-3/minicapstoneborja/minicapstone:$$time && \
	kubectl set image deployment minicapstone-borja minicapstone=us-east1-docker.pkg.dev/mlops-3/minicapstoneborja/minicapstone:$$time

auth:
	gcloud -q components update
	gcloud auth login
	gcloud -q config set project mlops-3
	gcloud -q auth configure-docker us-east1-docker.pkg.dev

create-infrastructure:
	gcloud container clusters create minicapstone-borja --num-nodes=1
	kubectl create deployment minicapstone-borja --image=us-east1-docker.pkg.dev/mlops-3/minicapstoneborja/minicapstone:latest
	kubectl expose deployment minicapstone-borja --type LoadBalancer --port 80 --target-port 8000
