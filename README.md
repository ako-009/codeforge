# CodeForge

**Agentic Code Synthesis with Sandboxed Execution & Self-Repair**

> LangGraph · Docker · FastAPI · Streamlit · Groq API

---

## What it does

CodeForge receives a coding task in plain English and:

1. **Plans** an approach using an LLM
2. **Writes** Python code automatically
3. **Executes** it inside an isolated Docker sandbox (CPU + memory limits, no network, 10s timeout)
4. **Self-repairs** on failure — up to 3 attempts
5. **Runs regression tests** on repaired code before accepting it
6. **Returns** working code + output + full execution trace via FastAPI

---

## Architecture

User Task (English)
│
▼
FastAPI /execute
│
▼
LangGraph Agent
plan_node → code_node → sandbox_node → critic_node
│
┌─────────┴─────────┐
PASS FAIL
│ │
regression_node repair_node
│ │
output_node sandbox_node (retry)
│
▼
FastAPI Response: code + output + trace + metrics
│
▼
Streamlit Dashboard


---

## CV Bullet

CodeForge: Agentic Code Synthesis with Sandboxed Execution & Self-Repair
LangGraph, Docker, FastAPI, Streamlit, Groq API | Self Project [Sep 2026]

Engineered agentic code synthesis pipeline using LangGraph where LLM autonomously
writes, executes, and self-repairs Python code until correct output is achieved
Implemented Docker-based sandbox with CPU/memory limits, network isolation and
10-second timeout — safely executing untrusted LLM-generated code at runtime
Built regression test runner validating self-repaired code against original test
cases, achieving 100% task completion on 10-problem HumanEval subset
Deployed FastAPI backend with execution trace logging and Streamlit dashboard
for real-time task submission and benchmark visualisation

---

## Benchmark Results

| Metric | Result |
|--------|--------|
| Completion rate | 100% (10/10) |
| First-try rate | 100% |
| Avg iterations | 1.0 |
| Sandbox timeout | 10s enforced |

---

## Setup

### Prerequisites
- Python 3.11+
- Docker Desktop running
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

```bash
git clone https://github.com/ako-009/codeforge.git
cd codeforge
python -m venv venv
venv\Scripts\Activate.ps1       # Windows
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Build sandbox image

```bash
docker build -t codeforge-sandbox:latest ./sandbox_image
```

### Run

Terminal 1 — API:
```bash
uvicorn app.main:app --reload --port 8003
```

Terminal 2 — Dashboard:
```bash
streamlit run dashboard/streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/execute` | Run a task through the agent |
| GET | `/task/{task_id}` | Get result for a specific task |
| GET | `/history` | List all past tasks |
| GET | `/health` | Health check |

---

## Tech Stack

| Technology | Role |
|------------|------|
| LangGraph | Agent state machine |
| Groq API | LLM code generation |
| Docker SDK | Sandbox container management |
| FastAPI | REST API layer |
| Streamlit | Dashboard UI |
| pytest | Regression test runner |

---

## Interview Q&A

**Why Docker instead of Python exec()?**
exec() runs in the same process — malicious code can delete files or use unlimited memory. Docker containers are fully isolated at the OS level with enforced CPU, memory, and network limits.

**How does self-repair work?**
The LLM receives the original task + broken code + stderr. It rewrites the code fixing the specific error. The repaired code is re-executed in a fresh sandbox.

**What is regression testing here?**
After repair, the original test cases are re-run on the fixed code. Only if all pass is the repair accepted — preventing fixes that break prior behaviour.