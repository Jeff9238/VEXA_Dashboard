import os
import datetime
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
os.environ["OPENAI_API_KEY"] = "NA" # Bypass OpenAI checks

# 1. Setup Brain (Gemini 2.5 Flash)
# Note: "gemini-2.5-flash" is the latest. If it fails, fallback to "gemini-2.0-flash".
my_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# 2. Load the Rules
def load_global_rules():
    try:
        with open("global_rules.md", "r") as file:
            return file.read()
    except:
        return "STRICT MODE: Follow user instructions exactly. No filler."

rules = load_global_rules()

# 3. Define The Agents

# Agent A: The Architect (Planner)
architect = Agent(
    role='Chief Architect',
    goal='Plan strictly according to user constraints.',
    backstory=f"You are the guardian of the requirements. You ensure no rule is broken.\nRULES:\n{rules}",
    llm=my_llm,
    verbose=True
)

# Agent B: The Lead Engineer (Coder)
lead_dev = Agent(
    role='Lead Engineer',
    goal='Write production-ready, SEO-optimized code.',
    backstory=f"You write the actual code. You favor Full Code rewrites for clarity.\nRULES:\n{rules}",
    llm=my_llm,
    verbose=True
)

# Agent C: The Debugger (NEW!)
debugger = Agent(
    role='Senior Debugger',
    goal='Identify bugs, security risks, and logic errors.',
    backstory=f"You are a pessimist. You look for what will break. You analyze the code for SEO and Security flaws.\nRULES:\n{rules}",
    llm=my_llm,
    verbose=True
)

# 4. execution Engine & Auto-Save
def run_vexa_crew(user_request, project_mode="New Feature"):
    
    # Define Tasks based on mode
    tasks = []

    if project_mode == "Debugging / Fix":
        # Debugging Workflow
        debug_task = Task(
            description=f"Analyze this code/request for errors: {user_request}. Find the bug.",
            agent=debugger,
            expected_output="Analysis of the bug and the specific fix logic."
        )
        fix_task = Task(
            description="Apply the fix and provide the FULL corrected code file.",
            agent=lead_dev,
            expected_output="The complete, fixed code file."
        )
        tasks = [debug_task, fix_task]
    
    else:
        # Normal Feature Workflow
        plan_task = Task(
            description=f"Request: {user_request}. Create a strict technical plan.",
            agent=architect,
            expected_output="Technical Roadmap."
        )
        code_task = Task(
            description="Write the FULL code based on the plan. Ensure SEO and Security compliance.",
            agent=lead_dev,
            expected_output="Complete source code."
        )
        tasks = [plan_task, code_task]

    # Run Crew
    vexa_crew = Crew(
        agents=[architect, lead_dev, debugger],
        tasks=tasks,
        process=Process.sequential
    )
    
    result = vexa_crew.kickoff()

    # --- AUTO SAVE HISTORY ---
    # This saves every interaction to a file so you don't lose it.
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"history/log_{timestamp}.md"
    
    os.makedirs("history", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Request: {user_request}\n\n")
        f.write(str(result))
    
    return str(result)