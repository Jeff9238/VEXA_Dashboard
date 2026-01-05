import streamlit as st
from agents import run_vexa_crew
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="VEXA Manager", 
    layout="wide", 
    page_icon="💎"
)

# --- LIGHT MODE GLASSMORPHISM CSS ---
st.markdown("""
<style>
    /* 1. Global Background (Clean Light Gradient) */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        background-attachment: fixed;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #000000;
    }
    
    /* 2. Sidebar (Frosted White Glass) */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    /* Sidebar Text Fix */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p {
        color: #333333 !important;
    }

    /* 3. Glass Cards (White Translucent) */
    .glass-card {
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        margin-bottom: 20px;
    }

    /* 4. Inputs (Clean White) */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #000000 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 12px !important;
        font-weight: 500;
    }
    
    /* Focus State */
    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus {
        border: 1px solid #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
    }

    /* 5. Buttons (Professional Blue) */
    .stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
        color: white !important;
    }

    /* 6. File Uploader */
    [data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.5);
        border: 2px dashed #9ca3af;
        border-radius: 15px;
        padding: 15px;
    }
    [data-testid="stFileUploader"] small {
        color: #4b5563 !important;
    }

    /* Titles & Text */
    h1, h2, h3 {
        color: #111827 !important; /* Almost Black */
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    
    p, label, .stMarkdown {
        color: #374151 !important; /* Dark Grey */
    }
    
    /* Code Blocks */
    code {
        color: #d946ef;
        background-color: #f3f4f6;
    }
    
    /* Success/Info Messages */
    .stSuccess, .stInfo, .stWarning, .stError {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(0,0,0,0.05);
        color: #1f2937 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Light Panel) ---
with st.sidebar:
    st.markdown("## 💎 VEXA OS")
    st.caption("v3.1 Light Edition | IT Manager Dashboard")
    st.write("---")
    
    # Mode Selector
    st.markdown("### ⚙️ Protocol")
    mode = st.radio(
        "Select Operation Mode:", 
        ["New Feature", "Debugging / Fix", "Direct File Edit (Trae Mode)"],
        label_visibility="collapsed"
    )
    
    st.write("---")
    
    # Dynamic Info Box
    if mode == "Direct File Edit (Trae Mode)":
        st.error("🔥 **READ/WRITE ACCESS**\nAgents will modify your hard drive directly.")
    elif mode == "Debugging / Fix":
        st.info("🛡️ **DEBUGGER ACTIVE**\nScanning for logic & security flaws.")
    else:
        st.success("✨ **CREATOR MODE**\nArchitecting new solutions.")

    st.write("---")
    
    # Workspace Stats
    st.markdown("### 📂 Workspace")
    py_files = [f for f in os.listdir('.') if f.endswith('.py')]
    st.caption(f"Tracking {len(py_files)} Python Modules")
    if st.button("🔄 Refresh Index"):
        st.toast("Workspace synced successfully.")

# --- MAIN LAYOUT ---

# Header Section
st.markdown("<h1 style='text-align: center; margin-bottom: 10px; color: #1e3a8a;'>VEXA INTELLIGENCE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 40px; color: #4b5563;'>Orchestrating 4 Autonomous Agents</p>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

# LEFT COLUMN: Input & Controls
with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 1. Context Injection")
    
    uploaded_file = st.file_uploader("Drop code files here to analyze", type=['py', 'js', 'md', 'txt', 'json'], label_visibility="collapsed")
    
    file_content = ""
    if uploaded_file:
        file_content = f"\n\n--- ATTACHED FILE: {uploaded_file.name} ---\n{uploaded_file.read().decode('utf-8')}\n----------------\n"
        st.success(f"📎 Linked: {uploaded_file.name}")
    
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 2. Command Center")
    with st.form("dev_form"):
        # Dynamic Placeholder
        if mode == "Direct File Edit (Trae Mode)":
            placeholder = "e.g. 'Read agents.py and add a FileDeleteTool. Save the changes.'"
        elif mode == "Debugging / Fix":
            placeholder = "e.g. 'Find why the API call is failing in the attached file.'"
        else:
            placeholder = "e.g. 'Design a modern dashboard layout for the VEXA admin panel.'"
            
        user_input = st.text_area("Instructions", height=120, placeholder=placeholder, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn2:
            submitted = st.form_submit_button("⚡ Initialize Agents")
    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT COLUMN: History & Status
with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🧠 Memory Log")
    if os.path.exists("history"):
        logs = sorted(os.listdir("history"), reverse=True)[:4]
        for log in logs:
            st.code(f"{log}", language="text")
    else:
        st.caption("No mission history found.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📡 Status")
    st.caption("Gemini 2.0 Flash: **ONLINE**")
    st.caption("File System Access: **GRANTED**")
    st.caption("Global Rules: **STRICT**")
    st.markdown("</div>", unsafe_allow_html=True)

# --- OUTPUT SECTION ---
if submitted and user_input:
    # Anchor for scrolling
    st.markdown("---")
    st.subheader("📦 Mission Output")
    
    final_prompt = user_input + file_content
    
    # A cleaner looking spinner
    with st.spinner(f"Agents are executing protocol: {mode}..."):
        try:
            result = run_vexa_crew(final_prompt, project_mode=mode)
            
            # Result Card
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            if mode == "Direct File Edit (Trae Mode)":
                st.balloons()
                st.success("File System Updated.")
            
            st.markdown(result)
            st.markdown("</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Execution Error: {e}")