import typer

from ..core import executor, observers, planner
from ..memory import episodic_store

app = typer.Typer(name="infra-agent")


@app.command()
def create_s3(
    env: str, name: str, apply: bool = typer.Option(False, "--apply")
) -> None:
    """Create a private S3 bucket in the target environment."""
    steps = []
    plan_out = planner.plan_s3_bucket(env, name)
    steps.append({"plan": plan_out})
    if apply:
        apply_out = executor.apply_s3_bucket(env, name)
        steps.append({"apply": apply_out})
        observed = observers.verify_s3_bucket(name)
        steps.append({"observe": observed})
    trace_path = episodic_store.write_trace(f"create_s3_{name}", steps)
    typer.echo(f"Trace written to {trace_path}")


if __name__ == "__main__":
    app()
