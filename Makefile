
init:
	$(MAKE) clear
	docker-compose build
	docker-compose up -d postgres
	sleep 4
	docker-compose run --rm web ./manage.py migrate
	# docker-compose run --rm web ./manage.py loaddata initial_data

clear:
	docker-compose stop
	docker-compose rm -f
	docker-compose ps
	docker ps

clear_all:
	docker stop $(shell docker ps -a -q)
	docker rm $(shell docker ps -a -q)

shell:
	docker-compose run --rm web bash

run:
	docker-compose up web

npm_install:
	docker run -it --rm --privileged=true -v $(shell pwd)/layout:/data -v $(shell pwd)/app:/app -v $(shell pwd)/app:/srv/app miguelalvarezi/nodejs-bower-gulp sh -c 'npm install && bower i --allow-root --config.interactive=false'

watch:
	docker run -it --rm --privileged=true -v $(shell pwd)/layout:/data -v $(shell pwd)/app:/app -v $(shell pwd)/app:/srv/app miguelalvarezi/nodejs-bower-gulp sh -c 'gulp'

npm:
	docker run -it --rm --privileged=true -v $(shell pwd)/layout:/data -v $(shell pwd)/app:/app -v $(shell pwd)/app:/srv/app miguelalvarezi/nodejs-bower-gulp bash
