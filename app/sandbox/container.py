# app/sandbox/container.py
# Utility to check Docker is available before we try to use it.

import docker

def get_docker_client():
    """
    Returns a Docker client, or raises a clear error if Docker is not running.
    """
    try:
        client = docker.from_env()
        client.ping()
        return client
    except Exception:
        raise RuntimeError(
            "Docker is not running or not accessible. "
            "Please start Docker Desktop and try again."
        )
