# dashboard/streamlit_app.py
import streamlit as st
import requests
import json

API_URL = "http://localhost:8003"

st.set_page_config(
    page_title="CodeForge",
    page_icon="forge",
    layout="wide"
)

st.title("CodeForge")
st.caption("Agentic Code Synthesis with Sandboxed Execution & Self-Repair")

# --- Sidebar ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Submit Task", "Task History", "Benchmark Results"])


# --- Page 1: Submit Task ---
if page == "Submit Task":
    st.header("Submit a Coding Task")

    task = st.text_area(
        "Task description",
        placeholder="e.g. Write a Python function to find all prime numbers up to 50 and print them",
        height=100
    )

    st.subheader("Test Cases (optional)")
    st.caption("If provided, repaired code must pass all test cases before being accepted.")

    num_tests = st.number_input("Number of test cases", min_value=0, max_value=5, value=0)
    test_cases = []
    for i in range(int(num_tests)):
        col1, col2 = st.columns(2)
        with col1:
            inp = st.text_input(f"Test {i+1} input", key=f"input_{i}")
        with col2:
            exp = st.text_input(f"Test {i+1} expected output", key=f"expected_{i}")
        if inp and exp:
            test_cases.append({"input": inp, "expected": exp})

    if st.button("Run CodeForge", type="primary"):
        if not task.strip():
            st.error("Please enter a task.")
        else:
            with st.spinner("Running agent... (this takes 10-30 seconds)"):
                try:
                    response = requests.post(
                        f"{API_URL}/execute",
                        json={"task": task, "test_cases": test_cases},
                        timeout=120
                    )
                    result = response.json()

                    # --- Results ---
                    st.divider()

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Success", "YES" if result["success"] else "NO")
                    col2.metric("Attempts", result["total_iterations"])
                    col3.metric("Regression", "PASS" if result["regression_passed"] else "FAIL")

                    st.subheader("Final Output")
                    st.code(result["final_output"], language="text")

                    st.subheader("Final Code")
                    st.code(result["final_code"], language="python")

                    st.subheader("Execution Trace")
                    for entry in result["execution_trace"]:
                        with st.expander(f"Attempt {entry['attempt']} — exit code {entry['exit_code']}"):
                            st.code(entry["code"], language="python")
                            if entry["stdout"]:
                                st.success(f"stdout: {entry['stdout']}")
                            if entry["stderr"]:
                                st.error(f"stderr: {entry['stderr']}")

                    if result["repair_history"]:
                        st.subheader("Self-Repair History")
                        for repair in result["repair_history"]:
                            with st.expander(f"Repair attempt {repair['attempt']}"):
                                st.text("Error that triggered repair:")
                                st.error(repair["error"])

                except Exception as e:
                    st.error(f"Error contacting API: {e}")


# --- Page 2: Task History ---
elif page == "Task History":
    st.header("Task History")

    try:
        response = requests.get(f"{API_URL}/history", timeout=10)
        history = response.json()

        if not history:
            st.info("No tasks run yet. Submit a task first.")
        else:
            for item in reversed(history):
                status = "SUCCESS" if item["success"] else "FAILED"
                color = "green" if item["success"] else "red"
                st.markdown(f"**:{color}[{status}]** — {item['task']} *(iterations: {item['total_iterations']})*")
                st.caption(f"Task ID: {item['task_id']}")
                st.divider()
    except Exception as e:
        st.error(f"Could not reach API: {e}. Is the FastAPI server running?")


# --- Page 3: Benchmark Results ---
elif page == "Benchmark Results":
    st.header("HumanEval Benchmark Results")

    try:
        with open("data/benchmark_results.json", "r") as f:
            report = json.load(f)

        metrics = report["metrics"]
        results = report["results"]

        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Completion Rate", f"{metrics['completion_rate']*100:.1f}%")
        col2.metric("Problems Passed", f"{metrics['passed']}/{metrics['total_problems']}")
        col3.metric("Avg Iterations", metrics["avg_iterations"])
        col4.metric("First-Try Rate", f"{metrics['first_try_rate']*100:.1f}%")

        # Results table
        st.subheader("Per-Problem Results")
        for r in results:
            status = "PASS" if r["success"] else "FAIL"
            color = "green" if r["success"] else "red"
            st.markdown(
                f"**:{color}[{status}]** {r['task_id']} — "
                f"{r['total_iterations']} iter, {r['elapsed_seconds']}s "
                f"| expected: `{r['expected']}` | actual: `{r['actual']}`"
            )

        # Bar chart
        st.subheader("Iterations per Problem")
        chart_data = {r["task_id"]: r["total_iterations"] for r in results}
        st.bar_chart(chart_data)

    except FileNotFoundError:
        st.warning("No benchmark results found. Run `python test_benchmark.py` first.")
    except Exception as e:
        st.error(f"Error loading results: {e}")