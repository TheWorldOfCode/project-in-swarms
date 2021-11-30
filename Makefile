image ?= swarm:dev
test_image ?= swarm:test
container_id_file ?= ./container_id
name ?= swarm_development


build:
	docker build -t $(image) -f .docker/dev.dockerfile .
	docker build -t $(test_image) -f .docker/experiment.dockerfile . 

buildrm:
	docker rmi $(image)

$(container_id_file):
	xhost local:docker
	docker run -it \
		--cidfile $(container_id_file) \
		--device /dev/dri:/dev/dri \
		-e DISPLAY \
		--workdir=/home/swarm/package \
		-v $(shell pwd):/home/swarm/package \
		-v $(HOME)/.vim:/home/swarm/.vim \
		-e QT_X11_NO_MITSHM=1 \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-v ~/.Xauthority:/root/.Xauthority \
		-v /run/user/1000:/run/user/1000 \
		-e XDG_RUNTIME_DIR \
		--name $(name) \
		$(image) 
	
start: $(container_id_file)
	xhost local:docker
	docker container start $(shell cat $(container_id_file) )

stop:
	docker container stop $(shell cat $(container_id_file) )

rm:
	docker container stop $(shell cat $(container_id_file) )
	docker container rm $(shell cat $(container_id_file) )
	rm $(container_id_file)

enter: $(container_id_file)
	docker exec -it $(shell cat $(container_id_file)) vim

setup_test:
	@./experiments/setup_experiments.sh ./experiments/map_1 ./experiments/templates/ "(10, 20)" 1 "(1, 10)" 0
	@bash ./experiments/setup_parallel map_1 30 map_1_parallel

setup_final_test:
	@./experiments/setup_final_test ./experiments/final_test ./experiments/templates/ 0.6 0.8 0.2 20 20
	@./experiments/setup_parallel final_test 30 final_test_parallel

.PHONY: build buildrm create start stop rm enter setup_test setup_final_test
