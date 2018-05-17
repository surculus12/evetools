TAG ?= evetools:latest

build:
	docker build -t ${TAG} -f ./src/Dockerfile .
