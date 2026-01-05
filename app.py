import streamlit as st
from agents import run_vexa_crew
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="VEXA Dev Environment", 
    layout="wide", 
    page_icon="💻"
)

# --- CUSTOM CSS (Hacker / Dark Mode Vibe) ---
st.markdown("""
<style>
    .stTextInput > div > div > input {background-color: #0e1117; color: white; border: 1px solid #303030;}
    .stTextArea > div > div > textarea {background-color: #0e1117; color: white; border: 1px solid #303030;}
    .stButton > button {width: 100%; border-radius: 5px; font-weight: bold; background-color: #262730; color: white;}
    .stButton > button:hover {background-color: #0055FF; color: white;}
    .stSuccess {background-color: #1e252b;}
    [data-testid="stFileUploader"] {padding: 10px; border: 1px dashed #444; border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Controls) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9084/9084172.png", width=60)
    st.title("VEXA Workspace")
    st.write("---")
    
    # 1. Mode Selector
    st.subheader("🛠️ Operation Mode")
    mode = st.radio(
        "Select Protocol:", 
        ["New Feature", "Debugging / Fix"],
        captions=["Architect + Dev + SEO", "Debugger + Dev Only"]
    )
    
    st.write("---")
    
    # 2. Status Indicators
    st.subheader("📊 System Status")
    st.caption("✅ Active Model: Gemini 2.0 Flash")
    st.caption("✅ Auto-Save: ON (/history)")
    st.caption("✅ File Reader: ACTIVE")
    
    # 3. Help Section
    with st.expander("Help / Tips"):
        st.markdown("""
        - **New Feature:** Use for planning & building from scratch.
        - **Debugging:** Upload a file and ask "Find the bug".
        - **Files:** Supports .py, .js, .txt, .md, .json
        """)

# --- MAIN INTERFACE ---
st.title("💻 VEXA: Elite Coding Team")

# Create layout
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### Initialize Task")
    
    # --- NEW FEATURE: File Uploader ---
    # This sits outside the form so it updates immediately when you drop a file
    uploaded_file = st.file_uploader("📂 Load Context File (Optional - Drag & Drop code here)", type=['py', 'js', 'md', 'txt', 'json', 'dart', 'html', 'css'])
    
    file_context_msg = ""
    file_content = ""
    
    if uploaded_file is not None:
        try:
            # Read file content
            raw_content = uploaded_file.read().decode("utf-8")
            # Format it for the Agent
            file_content = f"\n\n--- ATTACHED FILE: {uploaded_file.name} ---\n{raw_content}\n----------------------------------\n"
            st.success(f"✅ Loaded: {uploaded_file.name}")
        except Exception as e:
            st.error(f"Error reading file: {e}")

    with st.form("dev_form"):
        # Dynamic Placeholder
        if mode == "Debugging / Fix":
            placeholder_text = "Instructions: 'Find the logic error in the attached file' or 'Secure this API endpoint'..."
        else:
            placeholder_text = "Instructions: 'Build a login screen using Chemlite colors'..."
            
        user_input = st.text_area("Manager Instructions:", height=150, placeholder=placeholder_text)
        
        # Submit Button
        submitted = st.form_submit_button("⚡ Execute Agents")

with col2:
    st.info("💡 **Pro Tip:**\nAlways upload your existing file when asking for changes. The agents need to see the code to fix it.")
    st.warning("⚠️ **Rules Active:**\nAgents strictly follow 'global_rules.md'. No marketing fluff.")

# --- EXECUTION LOGIC ---
if submitted and user_input:
    st.write("---")
    
    # Combine User Input + File Content
    final_prompt = user_input + file_content
    
    # 1. Show Progress Spinner
    with st.spinner(f"Agents are running protocol: {mode}..."):
        try:
            # 2. Call the Agents
            result = run_vexa_crew(final_prompt, project_mode=mode)
            
            # 3. Success Message
            st.success("✅ Task Completed Successfully")
            
            # 4. Show Save Location
            # Find the newest file in history folder
            if os.path.exists("history"):
                files = os.listdir("history")
                if files:
                    files.sort(key=lambda x: os.path.getmtime(os.path.join("history", x)), reverse=True)
                    latest_file = files[0]
                    st.caption(f"📁 Conversation saved to: history/{latest_file}")
            
            # 5. Display Output
            st.markdown("### 📦 Agent Output")
            st.markdown(result)
            
        except Exception as e:
            st.error(f"❌ System Error: {e}")
            st.info("Troubleshooting: Check your Internet connection or API Key in .env")

# --- FOOTER ---
st.write("---")
st.caption("VEXA Internal Dashboard v2.1 | Powered by CrewAI & Gemini")