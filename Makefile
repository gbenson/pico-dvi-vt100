all: build-in-docker

build-in-docker:
	docker run --rm -it \
		--mount type=bind,source=${PWD},target=/home/dev \
		--workdir /home/dev \
		--user $(shell id -u):$(shell id -g) \
		--env PICO_PLATFORM=rp2350-arm-s \
		lukstep/raspberry-pi-pico-sdk \
	    make build

build: software/build/Makefile
	make -C software/build

software/build/Makefile: software/CMakeLists.txt
	mkdir -p software/build
	cd software/build && cmake \
		-DDVI_DEFAULT_SERIAL_CONFIG=waveshare_pico_dvi_cfg \
		..

