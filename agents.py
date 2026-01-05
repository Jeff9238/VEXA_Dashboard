import os
import datetime
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileReadTool, FileWriterTool, DirectoryReadTool
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
os.environ["OPENAI_API_KEY"] = "NA" 

# 1. SETUP BRAINS (Hybrid Engine 2.5)
# The "Thinker" - Logic & Planning
smart_llm = LLM(
    model="gemini/gemini-2.5-pro",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)

# The "Doer" - Speed & Coding
fast_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1
)

# 2. SETUP TOOLS (With Safety Rails)
file_read_tool = FileReadTool()
file_write_tool = FileWriterTool()
# We force the directory tool to prefer looking at a 'project' subfolder if possible, 
# but for now, we rely on the Prompt Rules to avoid app.py
directory_tool = DirectoryReadTool(directory='./') 

# 3. LOAD RULES
def load_global_rules():
    try:
        with open("global_rules.md", "r") as file:
            return file.read()
    except:
        return "STRICT MODE: Do not edit app.py or agents.py."

rules = load_global_rules()

# 4. DEFINE AGENTS

# Agent A: The Architect (Smart Brain)
architect = Agent(
    role='Chief Architect',
    goal='Plan the project steps and folder structure.',
    backstory=f"""You represent the 'Step-by-Step' guide. You never write code immediately. 
    You first tell the user what needs to be installed and created.
    CRITICAL: YOU MUST IGNORE 'app.py' and 'agents.py'. They are system files.
    RULES:\n{rules}""",
    llm=fast_llm, 
    tools=[directory_tool, file_read_tool],
    verbose=True
)

# Agent B: The Lead Engineer (Fast Brain)
lead_dev = Agent(
    role='Lead Engineer',
    goal='Write production code and implement the plan.',
    backstory=f"""You write the actual code files. 
    You present code clearly for the 'Canvas' view.
    CRITICAL: NEVER EDIT 'app.py'. If asked to 'update the app', update the USER'S project files.
    RULES:\n{rules}""",
    llm=fast_llm, 
    tools=[file_read_tool, file_write_tool],
    verbose=True
)

# Agent C: The Debugger (Smart Brain)
debugger = Agent(
    role='Senior Debugger',
    goal='Analyze code for security and logic flaws.',
    backstory=f"""You check for bugs and security risks. 
    You ensure the user follows the installation steps.
    RULES:\n{rules}""",
    llm=fast_llm, 
    tools=[file_read_tool],
    verbose=True
)

# 5. EXECUTION ENGINE
def run_vexa_crew(user_request, project_mode="New Feature"):
    
    tasks = []

    # SAFETY CHECK IN PROMPT
    safety_instruction = "\n(REMINDER: Do not edit or analyze 'app.py' or 'agents.py'. Work on target project files only.)"
    full_request = user_request + safety_instruction

    if project_mode == "Direct File Edit (Trae Mode)":
        edit_task = Task(
            description=f"Request: {full_request}. \n1. Read the target file. \n2. Apply changes. \n3. CONFIRM you did not touch app.py.",
            agent=lead_dev,
            expected_output="Confirmation of modified files."
        )
        tasks = [edit_task]

    elif project_mode == "Debugging / Fix":
        debug_task = Task(
            description=f"Analyze: {full_request}. Provide a fix guide and the corrected code.",
            agent=debugger,
            expected_output="Step-by-step fix guide + Code blocks."
        )
        tasks = [debug_task]
    
    else:
        # Standard Plan -> Code
        plan_task = Task(
            description=f"Request: {full_request}. \nCreate a Step-by-Step Implementation Guide (commands, folders, files).",
            agent=architect,
            expected_output="Markdown Guide with Shell commands."
        )
        code_task = Task(
            description="Based on the guide, write the FULL code files. Use clear file paths.",
            agent=lead_dev,
            expected_output="Markdown Code Blocks."
        )
        tasks = [plan_task, code_task]

    vexa_crew = Crew(
        agents=[architect, lead_dev, debugger],
        tasks=tasks,
        process=Process.sequential
    )
    
    result = vexa_crew.kickoff()

    # Save Log
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    os.makedirs("history", exist_ok=True)
    with open(f"history/log_{timestamp}.md", "w", encoding="utf-8") as f:
        f.write(f"# Request: {user_request}\n\n{str(result)}")
    
    return str(result)