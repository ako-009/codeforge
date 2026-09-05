# app/sandbox/limits.py
# Resource limits for the Docker sandbox container.
# These mirror what production code execution platforms use.

SANDBOX_IMAGE = "codeforge-sandbox:latest"

# Time limit — container is killed after this many seconds
TIMEOUT_SECONDS = 10

# Memory limit — container cannot use more than this
MEMORY_LIMIT = "128m"

# CPU limits — container gets at most 50% of one CPU core
# cpu_period is the scheduling window in microseconds (100ms)
# cpu_quota is how much of that window the container can use (50ms = 50%)
CPU_PERIOD = 100000
CPU_QUOTA = 50000
