# ScaleNyx

AI infrastructure agent monorepo.

## Development

```bash
make dev
make test
```

## Terraform CI

Pull requests against Terraform modules run policy checks and cost guardrails:

* OPA/Conftest policies under `security/opa`
* Infracost comments with failure when cost increases exceed
  `INFRACOST_THRESHOLD` (default 20%)
* Scheduled drift detection using `terraform plan -refresh-only`

## CLI

Create an S3 bucket:

```bash
infra-agent create-s3 --env dev --name demo-bucket --apply
```
