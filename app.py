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
    .stButton > button {width: 100%; border-radius: 5px; font-weight: bold;}
    .stSuccess {background-color: #1e252b;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Controls) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9084/9084172.png", width=60)
    st.title("VEXA Workspace")
    st.write("---")
    
    # 1. Mode Selector (New Feature vs Debugging)
    st.subheader("🛠️ Operation Mode")
    mode = st.radio(
        "Select Agent Protocol:", 
        ["New Feature", "Debugging / Fix"],
        captions=["Architect + Dev + SEO", "Debugger + Dev Only"]
    )
    
    st.write("---")
    
    # 2. Status Indicators
    st.subheader("📊 System Status")
    st.caption(f"✅ Active Model: Gemini 2.5 Flash")
    st.caption("✅ Auto-Save: ON (/history folder)")
    st.caption("✅ Strict Rules: global_rules.md")

# --- MAIN INTERFACE ---
st.title("💻 VEXA: Elite Coding Team")

# Create two columns for layout
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### Initialize Task")
    with st.form("dev_form"):
        # Dynamic Placeholder based on mode
        if mode == "Debugging / Fix":
            placeholder_text = "Paste the broken code here and explain the error..."
        else:
            placeholder_text = "Example: Build a React Native 'Vehicle Inspection' screen with a camera button. Use Chemlite dark theme."
            
        user_input = st.text_area("Input Instructions:", height=200, placeholder=placeholder_text)
        
        # Submit Button
        submitted = st.form_submit_button("⚡ Execute Agents")

with col2:
    st.info("💡 **Pro Tip:**\nFor best results, paste your existing file content if you want the agents to modify it.")
    st.warning("⚠️ **Rules Active:**\nAgents will refuse to generate filler text or marketing fluff.")

# --- EXECUTION LOGIC ---
if submitted and user_input:
    st.write("---")
    
    # 1. Show Progress Spinner
    with st.spinner(f"Agents are running protocol: {mode}..."):
        try:
            # 2. Call the Agents (Passing the Mode)
            result = run_vexa_crew(user_input, project_mode=mode)
            
            # 3. Success Message
            st.success("✅ Task Completed Successfully")
            
            # 4. Show Save Location
            files = os.listdir("history")
            files.sort(key=lambda x: os.path.getmtime(os.path.join("history", x)), reverse=True)
            latest_file = files[0] if files else "Unknown"
            st.caption(f"📁 Conversation saved to: history/{latest_file}")
            
            # 5. Display the Output
            st.markdown("### 📦 Agent Output")
            st.markdown(result)
            
        except Exception as e:
            st.error(f"❌ System Error: {e}")
            st.error("Check your API Key or Internet Connection.")

# --- FOOTER ---
st.write("---")
st.caption("VEXA Internal Tool v2.0 | Powered by CrewAI & Gemini")