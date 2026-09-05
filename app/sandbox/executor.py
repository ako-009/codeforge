# app/sandbox/executor.py
import docker
import tempfile
import os
from app.sandbox.limits import (
    SANDBOX_IMAGE, TIMEOUT_SECONDS, MEMORY_LIMIT, CPU_PERIOD, CPU_QUOTA
)

def execute_code(code: str) -> dict:
    """
    Run a string of Python code inside an isolated Docker container.

    Analogy: like running a reaction in a sealed fume hood.
    - The code is written to a temp file (the reagent)
    - Mounted read-only into the container (loaded into the hood)
    - Container runs it with resource limits (hood safety controls)
    - stdout/stderr captured (reaction readout)
    - Container destroyed after run (hood cleaned)

    Returns:
        {
            stdout: str,      # printed output
            stderr: str,      # error messages
            exit_code: int,   # 0 = success, non-zero = error
            timed_out: bool   # True if killed after 10s
        }
    """
    client = docker.from_env()

    # Write code to a temporary file on the host machine
    # We'll mount this file into the container at /code/solution.py
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.py',
        delete=False,
        encoding='utf-8'
    ) as f:
        f.write(code)
        code_path = f.name

    try:
        # Spin up a container with all safety limits applied
        container = client.containers.run(
            image=SANDBOX_IMAGE,
            command="python /code/solution.py",
            volumes={
                code_path: {
                    "bind": "/code/solution.py",
                    "mode": "ro"   # read-only — container cannot modify the file
                }
            },
            mem_limit=MEMORY_LIMIT,
            cpu_period=CPU_PERIOD,
            cpu_quota=CPU_QUOTA,
            network_disabled=True,   # no internet access
            detach=True,             # run in background so we can apply timeout
            remove=False             # we'll remove manually after reading logs
        )

        try:
            # Wait for container to finish, with timeout
            result = container.wait(timeout=TIMEOUT_SECONDS)
            stdout = container.logs(stdout=True, stderr=False).decode('utf-8', errors='replace')
            stderr = container.logs(stdout=False, stderr=True).decode('utf-8', errors='replace')
            return {
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": result["StatusCode"],
                "timed_out": False
            }

        except Exception:
            # Timeout hit — kill the container
            container.kill()
            return {
                "stdout": "",
                "stderr": "Execution timed out after 10 seconds.",
                "exit_code": -1,
                "timed_out": True
            }

        finally:
            # Always remove the container, even if we killed it
            try:
                container.remove(force=True)
            except Exception:
                pass

    finally:
        # Always delete the temp file from host
        try:
            os.unlink(code_path)
        except Exception:
            pass
