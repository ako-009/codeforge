# app/llm/prompts.py
# All prompt templates used by CodeForge.
# A prompt is just a string with placeholders — like a lab procedure template.

PLAN_PROMPT = """You are an expert Python programmer and problem solver.

TASK: {task}

Break this task into a clear, numbered step-by-step plan.
Be concise. Maximum 5 steps.
Return ONLY the numbered plan, no extra explanation."""


CODE_GEN_PROMPT = """You are an expert Python programmer.

TASK: {task}

PLAN:
{plan}

Write a complete Python solution. Requirements:
- Return ONLY Python code, no markdown, no explanation, no triple backticks
- Include a main block that prints the result
- Handle edge cases
- Code must be immediately runnable

Python code:"""


REPAIR_PROMPT = """You are an expert Python debugger.

ORIGINAL TASK:
{task}

YOUR PREVIOUS CODE (attempt {attempt}):
{code}

ERROR RECEIVED:
{stderr}

STDOUT BEFORE ERROR:
{stdout}

Fix the code. Return ONLY the corrected Python code.
No explanation, no markdown, no triple backticks.
The fixed code must:
1. Solve the original task
2. Fix the specific error above
3. Be complete and runnable

Fixed Python code:"""
