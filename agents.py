import os
import datetime
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileReadTool, FileWriterTool, DirectoryReadTool
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
os.environ["OPENAI_API_KEY"] = "NA" 

# 1. SETUP BRAINS (The Hybrid Engine)

# BRAIN A: The "Thinker" (For Planning & Logic)
# Uses the powerful 2.5 Pro model for complex reasoning
smart_llm = LLM(
    model="gemini/gemini-2.5-pro",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)

# BRAIN B: The "Doer" (For Speed & Volume)
# Uses the 2.5 Flash model for fast coding
fast_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1
)

# 2. Setup Tools (The Hands & Eyes)
# These allow agents to interact with your actual hard drive.
file_read_tool = FileReadTool()
file_write_tool = FileWriterTool()
directory_tool = DirectoryReadTool(directory='./') # Scans current folder

# 3. Load Rules
def load_global_rules():
    try:
        with open("global_rules.md", "r") as file:
            return file.read()
    except:
        return "STRICT MODE: Follow user instructions exactly."

rules = load_global_rules()

# 4. Define The Agents

# Agent A: The Architect (Now sees the folder structure)
architect = Agent(
    role='Chief Architect',
    goal='Analyze project structure and plan features.',
    backstory=f"You scan the folder structure first. You ensure new files fit the existing architecture.\nRULES:\n{rules}",
    llm=smart_llm,
    tools=[directory_tool, file_read_tool], # Can see folders
    verbose=True
)

# Agent B: The Lead Engineer (Now writes files)
lead_dev = Agent(
    role='Lead Engineer',
    goal='Write code and SAVE it to the file system.',
    backstory=f"You are authorized to WRITE code to files. Always create a backup before overwriting.\nRULES:\n{rules}",
    llm=fast_llm,
    tools=[file_read_tool, file_write_tool], # Can write files
    verbose=True
)

# Agent C: The Debugger
debugger = Agent(
    role='Senior Debugger',
    goal='Read files, find bugs, and propose fixes.',
    backstory=f"You read the actual file content to find logical errors.\nRULES:\n{rules}",
    llm=smart_llm,
    tools=[file_read_tool], # Can read files
    verbose=True
)

# 5. Execution Engine
def run_vexa_crew(user_request, project_mode="New Feature"):
    
    tasks = []

    if project_mode == "Direct File Edit (Trae Mode)":
        # This mode gives the agent permission to edit files directly
        edit_task = Task(
            description=f"Request: {user_request}. \n1. READ the relevant file. \n2. WRITE the updated code directly to the file.",
            agent=lead_dev,
            expected_output="Confirmation that file has been updated."
        )
        tasks = [edit_task]

    elif project_mode == "Debugging / Fix":
        debug_task = Task(
            description=f"Analyze this request: {user_request}. Read the files in the directory to find the issue.",
            agent=debugger,
            expected_output="Analysis of the bug."
        )
        tasks = [debug_task]
    
    else:
        # Standard Plan -> Code mode
        plan_task = Task(
            description=f"Request: {user_request}. Scan the directory to understand the current structure first.",
            agent=architect,
            expected_output="Technical Roadmap."
        )
        code_task = Task(
            description="Write the FULL code. If the user asked to save it, use the FileWriteTool.",
            agent=lead_dev,
            expected_output="Complete source code."
        )
        tasks = [plan_task, code_task]

    vexa_crew = Crew(
        agents=[architect, lead_dev, debugger],
        tasks=tasks,
        process=Process.sequential
    )
    
    result = vexa_crew.kickoff()

    # Auto-Save Log
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"history/log_{timestamp}.md"
    os.makedirs("history", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Request: {user_request}\n\n{str(result)}")
    
    return str(result)