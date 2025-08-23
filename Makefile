dev:
	bash scripts/dev_bootstrap.sh

test:
	pre-commit run --all-files
	pytest

fmt:
	pre-commit run --all-files

lint:
	ruff src tests

docker:
	docker build -t scalenyx-agent -f docker/agent.Dockerfile .

tf-plan:
	scripts/tf_wrapper.sh plan infra/terraform/live/dev/s3

tf-apply:
	scripts/tf_wrapper.sh apply infra/terraform/live/dev/s3
