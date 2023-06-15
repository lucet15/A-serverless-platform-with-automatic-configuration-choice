NAME:=faas-grafana-m1
VERSION:=4.6.3
DOCKER_REPOSITORY:=lucet
DOCKER_IMAGE_NAME:=$(DOCKER_REPOSITORY)/$(NAME)

.PHONY: build
build:
	@cd grafana ; docker build --platform linux/amd64 -t $(DOCKER_IMAGE_NAME):$(VERSION) .

.PHONY: push
push:
	@docker push $(DOCKER_IMAGE_NAME):$(VERSION)
