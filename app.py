# app.py
# =====================================================================
# Frontend — Streamlit UI
# AI Test Suite Studio — Quality Assurance Test Case Generator
# =====================================================================

import streamlit as st
import streamlit.components.v1 as components
import requests

# =====================================================================
# CONFIGURATION
# =====================================================================
import os
BACKEND_BASE = os.getenv("BACKEND_BASE_URL", "http://127.0.0.1:8000")
BACKEND_URL = f"{BACKEND_BASE}/generate"
DOWNLOAD_URL = f"{BACKEND_BASE}/download"


# =====================================================================
# PAGE CONFIGURATION
# =====================================================================
st.set_page_config(
    page_title="AI Test Suite Studio",
    page_icon="🧪",
    layout="wide"
)

# =====================================================================
# CUSTOM CSS
# =====================================================================
st.markdown("""
    <style>
        .stApp {
            background-color: #F5F5F7;
        }
        .main-header {
            background-color: #1E2761;
            padding: 18px 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .header-title {
            color: #FFFFFF;
            font-size: 20px;
            font-weight: 700;
        }
        .header-version {
            color: #02C39A;
            font-size: 13px;
            margin-left: 15px;
        }
        .header-sub {
            color: #CADCFC;
            font-size: 13px;
        }
        .section-title {
            color: #1A1A2E;
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 2px;
        }
        .section-sub {
            color: #6B7280;
            font-size: 13px;
            margin-bottom: 12px;
        }
        .stTextArea textarea {
            background-color: #F9F9FB !important;
            color: #1A1A2E !important;
            font-family: Consolas, monospace !important;
            border: 1px solid #E0E0E5 !important;
            border-radius: 6px !important;
        }
        .stButton > button {
            font-weight: 700 !important;
            border: none !important;
            border-radius: 8px !important;
            width: 100% !important;
            cursor: pointer !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #FFFFFF;
            border-radius: 8px;
            padding: 4px;
            border: 1px solid #E0E0E5;
        }
        .stTabs [data-baseweb="tab"] {
            color: #6B7280 !important;
            font-weight: 700 !important;
            font-size: 13px !important;
        }
        .stTabs [aria-selected="true"] {
            color: #0A84FF !important;
            background-color: #F9F9FB !important;
            border-radius: 6px !important;
        }
        .output-box {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E5;
            border-radius: 8px;
            padding: 15px;
            font-family: Consolas, monospace;
            font-size: 13px;
            color: #028090;
            white-space: pre-wrap;
            min-height: 250px;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# HEADER
# =====================================================================
st.markdown("""
    <div class="main-header">
        <div>
            <span class="header-title">AI Test Suite Studio</span>
            <span class="header-version">v1.0.0</span>
        </div>
        <span class="header-sub">Quality Assurance — Test Case Generator</span>
    </div>
""", unsafe_allow_html=True)

# =====================================================================
# COPY TO CLIPBOARD HELPER
# =====================================================================
def copy_button(text_to_copy, key):
    safe_text = text_to_copy.replace("`", "\\`").replace("\\", "\\\\")
    components.html(f"""
        <button onclick="navigator.clipboard.writeText(`{safe_text}`)"
            style="
                background-color:#FF9F0A;
                color:white;
                border:none;
                border-radius:6px;
                padding:8px 14px;
                font-weight:700;
                font-family: 'Segoe UI', sans-serif;
                font-size:13px;
                cursor:pointer;
                margin-bottom:8px;
            "
            onmouseover="this.style.backgroundColor='#E08800'"
            onmouseout="this.style.backgroundColor='#FF9F0A'">
            📋 Copy to Clipboard
        </button>
    """, height=45)

# =====================================================================
# SESSION STATE INITIALIZATION
# =====================================================================
for key in ["test_cases_output", "acceptance_output", "gherkin_output", "feature_file_content", "generated"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key != "generated" else False

# =====================================================================
# LAYOUT PLACEHOLDERS — define columns first, fill content after logic runs
# =====================================================================
left_col, right_col = st.columns([1, 1.8])

# ── Render the input box and button FIRST so we can read the click ────
with left_col:
    card = st.container(border=True)
    with card:
        st.markdown('<p class="section-title">Agile Requirement Context</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-sub">Paste your user story below.</p>', unsafe_allow_html=True)

        user_story = st.text_area(
            label="",
            value="As a customer,\nI want to reset my password,\nSo that I can regain access to my account.",
            height=280,
            key="user_story_input"
        )

        generate_clicked = st.button("Generate Test Cases", type="primary")

        download_placeholder = st.empty()

# =====================================================================
# GENERATION LOGIC — runs BEFORE we fill the download placeholder
# =====================================================================
if generate_clicked:
    if not user_story.strip():
        st.warning("Please enter a user story before generating.")
    else:
        with st.spinner("Connecting to AI backend..."):
            try:
                response = requests.post(BACKEND_URL, json={"story": user_story}, timeout=30)

                if response.status_code == 200:
                    data = response.json()

                    tc_output = "POSITIVE TEST CASES:\n\n"
                    for tc in data.get("positive_test_cases", []):
                        tc_output += f"  + {tc}\n"
                    tc_output += "\nNEGATIVE TEST CASES:\n\n"
                    for tc in data.get("negative_test_cases", []):
                        tc_output += f"  - {tc}\n"
                    tc_output += "\nEDGE TEST CASES:\n\n"
                    for tc in data.get("edge_test_cases", []):
                        tc_output += f"  * {tc}\n"

                    ac_output = "ACCEPTANCE CRITERIA:\n\n"
                    for ac in data.get("acceptance_criteria", []):
                        ac_output += f"  [ ] {ac}\n"

                    gherkin_output = f"Feature: {data.get('feature_name', 'Generated Feature')}\n\n"
                    for sc in data.get("gherkin_scenarios", []):
                        gherkin_output += f"  Scenario: {sc.get('title', '')}\n"
                        for step in sc.get("steps", []):
                            gherkin_output += f"    {step}\n"
                        gherkin_output += "\n"

                    st.session_state.test_cases_output = tc_output
                    st.session_state.acceptance_output = ac_output
                    st.session_state.gherkin_output = gherkin_output.strip()
                    st.session_state.generated = True

                    # ── Fetch the real .feature file from backend ──────
                    try:
                        dl_response = requests.get(DOWNLOAD_URL, timeout=10)
                        if dl_response.status_code == 200:
                            st.session_state.feature_file_content = dl_response.text
                        else:
                            st.session_state.feature_file_content = gherkin_output
                    except Exception:
                        st.session_state.feature_file_content = gherkin_output

                    st.success("Test cases generated successfully!")

                else:
                    st.error(f"Backend error: {response.status_code} — {response.text}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to backend.\n\n"
                    "Steps to fix:\n"
                    "1. Open a new terminal\n"
                    "2. Run: cd backend\n"
                    "3. Run: python -m uvicorn main:app --reload\n"
                    "4. Then click Generate Test Cases again"
                )
            except requests.exceptions.Timeout:
                st.error("Request timed out. Try again.")
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

# =====================================================================
# NOW fill the download button placeholder — state is fully up to date
# =====================================================================
if st.session_state.generated and st.session_state.feature_file_content:
    with download_placeholder:
        st.download_button(
            label="⬇ Download .feature File",
            data=st.session_state.feature_file_content,
            file_name="test_cases.feature",
            mime="text/plain",
            use_container_width=True
        )

# =====================================================================
# RIGHT COLUMN — Output Tabs
# =====================================================================
with right_col:
    tab1, tab2, tab3 = st.tabs(["Test Cases", "Acceptance Criteria", "Gherkin Specs"])

    with tab1:
        if st.session_state.test_cases_output:
            copy_button(st.session_state.test_cases_output, "copy_tc")
            st.code(st.session_state.test_cases_output, language=None)
        else:
            st.markdown('<div class="output-box">Generate test cases to see results here...</div>', unsafe_allow_html=True)

    with tab2:
        if st.session_state.acceptance_output:
            copy_button(st.session_state.acceptance_output, "copy_ac")
            st.code(st.session_state.acceptance_output, language=None)
        else:
            st.markdown('<div class="output-box">Generate test cases to see acceptance criteria here...</div>', unsafe_allow_html=True)

    with tab3:
        if st.session_state.gherkin_output:
            copy_button(st.session_state.gherkin_output, "copy_gh")
            st.code(st.session_state.gherkin_output, language="gherkin")
        else:
            st.markdown('<div class="output-box">Generate test cases to see Gherkin scenarios here...</div>', unsafe_allow_html=True)