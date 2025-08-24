# CI policy failure

When the Terraform CI workflow fails due to policy checks or cost guardrails:

1. Review the workflow logs in GitHub Actions to identify which step failed.
2. For OPA/Conftest violations, inspect `plan.json` and the policy outputs
   under `security/opa/`.
3. For Infracost failures, compare the cost diff comment on the PR. Adjust
   resources or update the `INFRACOST_THRESHOLD` if appropriate.
4. Re-run `make test` locally after fixes to validate before pushing.
