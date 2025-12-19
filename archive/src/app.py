import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from data_preprocessing import DataPreprocessor
from advanced_models import AdvancedModelTrainer
from report_generator import ForensicsReportGenerator
import base64
import json
from datetime import datetime

# --- Path Resolution ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

def get_path(relative_path):
    full_path = os.path.join(BASE_DIR, relative_path)
    return full_path if os.path.exists(full_path) else relative_path

# --- Page Config ---
st.set_page_config(page_title="CYBERSENTINEL", layout="wide", page_icon="🛡️", initial_sidebar_state="expanded")

# --- Session State ---
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# ============================================================================
# CYBERPUNK GLITCH THEME - High-Energy Hacker Aesthetic
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;600;700&family=Orbitron:wght@400;500;600;700;800;900&display=swap');
    
    :root {
        --void-black: #050505;
        --void-dark: #0a0a0a;
        --void-gray: #111111;
        --electric-cyan: #00F0FF;
        --hot-pink: #FF007F;
        --acid-green: #00FF9F;
        --neon-yellow: #FFFF00;
        --danger-red: #FF3366;
        --text-bright: #f0f0f0;
        --text-dim: #aaaaaa;
        --text-muted: #888888;
        --text-secondary: #999999;
    }
    
    * { 
        font-family: 'Fira Code', monospace; 
        letter-spacing: 0.5px;
    }
    
    /* ===== VOID BLACK BACKGROUND WITH NOISE ===== */
    .stApp {
        background: var(--void-black);
        background-image: 
            radial-gradient(ellipse at 20% 80%, rgba(0, 240, 255, 0.03) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, rgba(255, 0, 127, 0.03) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(0, 255, 159, 0.02) 0%, transparent 70%);
    }
    
    /* Animated Hex Grid */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='49' viewBox='0 0 28 49'%3E%3Cg fill-rule='evenodd'%3E%3Cg fill='%2300F0FF' fill-opacity='0.03'%3E%3Cpath d='M13.99 9.25l13 7.5v15l-13 7.5L1 31.75v-15l12.99-7.5zM3 17.9v12.7l10.99 6.34 11-6.35V17.9l-11-6.34L3 17.9zM0 15l12.98-7.5V0h-2v6.35L0 12.69v2.3zm0 18.5L12.98 41v8h-2v-6.85L0 35.81v-2.3zM15 0v7.5L27.99 15H28v-2.31h-.01L17 6.35V0h-2zm0 49v-8l12.99-7.5H28v2.31h-.01L17 42.15V49h-2z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.4;
        pointer-events: none;
        z-index: 0;
        animation: gridPulse 4s ease-in-out infinite;
    }
    
    @keyframes gridPulse {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.5; }
    }
    
    #MainMenu, footer { visibility: hidden; }
    
    /* ===== SIDEBAR TOGGLE BUTTON - Always Visible ===== */
    /* Style the expand arrow when sidebar is collapsed */
    [data-testid="collapsedControl"] {
        position: fixed !important;
        top: 10px !important;
        left: 10px !important;
        z-index: 999999 !important;
        color: #00F0FF !important;
        background: rgba(5, 5, 5, 0.95) !important;
        border: 2px solid #00F0FF !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        font-size: 1.2rem !important;
        cursor: pointer !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4), inset 0 0 10px rgba(0, 240, 255, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: rgba(0, 240, 255, 0.15) !important;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.6), inset 0 0 20px rgba(0, 240, 255, 0.2) !important;
        transform: scale(1.05) !important;
    }
    
    [data-testid="collapsedControl"] svg {
        fill: #00F0FF !important;
        stroke: #00F0FF !important;
    }
    
    /* Sidebar collapse button inside sidebar */
    button[kind="header"],
    [data-testid="stSidebarCollapseButton"] {
        color: #00F0FF !important;
        background: transparent !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        border-radius: 4px !important;
    }
    
    button[kind="header"]:hover,
    [data-testid="stSidebarCollapseButton"]:hover {
        background: rgba(0, 240, 255, 0.1) !important;
        border-color: #00F0FF !important;
    }
    
    /* ===== GLITCH TEXT ANIMATION ===== */
    @keyframes glitch {
        0%, 100% { text-shadow: 2px 0 #FF007F, -2px 0 #00F0FF; }
        25% { text-shadow: -2px 0 #FF007F, 2px 0 #00F0FF; }
        50% { text-shadow: 2px 2px #FF007F, -2px -2px #00F0FF; }
        75% { text-shadow: -2px 2px #FF007F, 2px -2px #00F0FF; }
    }
    
    @keyframes glitchSkew {
        0%, 100% { transform: skew(0deg); }
        20% { transform: skew(-0.5deg); }
        40% { transform: skew(0.5deg); }
        60% { transform: skew(0deg); }
        80% { transform: skew(-0.3deg); }
    }
    
    @keyframes textGlitch {
        0%, 90%, 100% { opacity: 1; transform: translate(0); }
        91% { opacity: 0.8; transform: translate(-2px, 1px); }
        92% { opacity: 1; transform: translate(2px, -1px); }
        93% { opacity: 0.9; transform: translate(-1px, 2px); }
        94% { opacity: 1; transform: translate(0); }
    }
    
    /* ===== HEADERS ===== */
    h1 {
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
        color: var(--electric-cyan) !important;
        text-transform: uppercase;
        letter-spacing: 4px;
        animation: glitch 3s infinite, textGlitch 5s infinite;
        text-shadow: 0 0 10px var(--electric-cyan), 0 0 20px var(--electric-cyan), 0 0 40px var(--electric-cyan);
    }
    
    h2 {
        font-family: 'Orbitron', sans-serif !important;
        color: var(--hot-pink) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        border-left: 3px solid var(--hot-pink);
        padding-left: 12px;
        text-shadow: 0 0 10px var(--hot-pink);
    }
    
    /* ===== SIDEBAR - HACKER TERMINAL ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(5, 5, 5, 0.98) 0%, rgba(10, 10, 10, 0.98) 100%);
        border-right: 1px solid var(--electric-cyan);
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.1), inset 0 0 50px rgba(0, 240, 255, 0.02);
    }
    
    section[data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0; right: 0;
        width: 1px; height: 100%;
        background: linear-gradient(180deg, transparent, var(--electric-cyan), var(--hot-pink), transparent);
        animation: scanLine 3s linear infinite;
    }
    
    @keyframes scanLine {
        0% { opacity: 0.3; }
        50% { opacity: 1; }
        100% { opacity: 0.3; }
    }
    
    /* ===== HOLLOW NEON BUTTONS ===== */
    .cyber-btn {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 14px 18px;
        margin: 8px 12px;
        background: transparent;
        border: 1px solid var(--electric-cyan);
        border-radius: 4px;
        color: var(--electric-cyan);
        font-family: 'Fira Code', monospace;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 2px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        text-shadow: 0 0 5px var(--electric-cyan);
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.1), inset 0 0 10px rgba(0, 240, 255, 0.05);
    }
    
    .cyber-btn::before {
        content: '>';
        margin-right: 4px;
        opacity: 0;
        transition: all 0.2s ease;
    }
    
    .cyber-btn::after {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 240, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .cyber-btn:hover {
        background: rgba(0, 240, 255, 0.1);
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.3), inset 0 0 20px rgba(0, 240, 255, 0.1);
        animation: glitchSkew 0.3s ease;
    }
    
    .cyber-btn:hover::before { opacity: 1; }
    .cyber-btn:hover::after { left: 100%; }
    
    .cyber-btn.active {
        background: linear-gradient(90deg, rgba(0, 240, 255, 0.15), rgba(255, 0, 127, 0.1));
        border-color: var(--hot-pink);
        color: var(--hot-pink);
        text-shadow: 0 0 10px var(--hot-pink);
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.2), inset 0 0 20px rgba(255, 0, 127, 0.05);
    }
    
    .cyber-btn.active::before { opacity: 1; content: '>>'; }
    
    /* Override Streamlit buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: 1px solid var(--electric-cyan) !important;
        color: var(--electric-cyan) !important;
        font-family: 'Fira Code', monospace !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(0, 240, 255, 0.1) !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.3) !important;
    }
    
    /* ===== GLASSMORPHISM CARDS WITH NEON BORDER ===== */
    .glass-card {
        background: rgba(10, 10, 10, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-left: 3px solid var(--hot-pink);
        border-radius: 8px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, var(--hot-pink), transparent);
    }
    
    .glass-card:hover {
        border-color: var(--electric-cyan);
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.15), 0 0 60px rgba(255, 0, 127, 0.05);
        transform: translateY(-2px);
    }
    
    /* ===== NEON METRIC CARDS ===== */
    .metric-cyber {
        background: rgba(5, 5, 5, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 240, 255, 0.3);
        border-left: 3px solid var(--hot-pink);
        border-radius: 6px;
        padding: 18px;
        text-align: center;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .metric-cyber::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--hot-pink), var(--electric-cyan), var(--acid-green));
        opacity: 0.5;
    }
    
    .metric-cyber:hover {
        border-color: var(--electric-cyan);
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
    }
    
    .metric-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.2;
        text-shadow: 0 0 15px currentColor;
    }
    
    .metric-label {
        font-family: 'Fira Code', monospace;
        font-size: 0.65rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 6px;
    }
    
    .metric-label::before { content: '> '; color: var(--electric-cyan); }
    
    /* ===== HEARTBEAT PULSE ANIMATION ===== */
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); opacity: 1; }
        14% { transform: scale(1.1); }
        28% { transform: scale(1); }
        42% { transform: scale(1.1); }
        70% { transform: scale(1); opacity: 0.8; }
    }
    
    .heartbeat { animation: heartbeat 1.5s ease-in-out infinite; }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: transparent !important;
        border: 2px solid var(--electric-cyan) !important;
        color: var(--electric-cyan) !important;
        border-radius: 4px !important;
        padding: 14px 28px !important;
        font-family: 'Fira Code', monospace !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        background: rgba(0, 240, 255, 0.15) !important;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.4), inset 0 0 20px rgba(0, 240, 255, 0.1) !important;
        text-shadow: 0 0 10px var(--electric-cyan) !important;
    }
    
    .stButton > button:active {
        transform: scale(0.98) !important;
    }
    
    /* ===== COMMAND-LINE TABLE HEADERS ===== */
    .stDataFrame thead th {
        font-family: 'Fira Code', monospace !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        color: var(--electric-cyan) !important;
        background: rgba(0, 240, 255, 0.05) !important;
    }
    
    .stDataFrame thead th::before { content: '> '; }
    
    .stDataFrame { 
        border-radius: 8px; 
        border: 1px solid rgba(0, 240, 255, 0.2);
        overflow: hidden;
    }
    
    .stDataFrame tbody td {
        font-family: 'Fira Code', monospace !important;
        color: var(--text-bright) !important;
    }
    
    /* ===== PROGRESS BAR ===== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--electric-cyan), var(--hot-pink), var(--acid-green)) !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.5) !important;
    }
    
    /* ===== FILE UPLOADER ===== */
    .stFileUploader {
        background: rgba(5, 5, 5, 0.8);
        border: 2px dashed var(--electric-cyan);
        border-radius: 8px;
        padding: 30px;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: var(--hot-pink);
        box-shadow: 0 0 30px rgba(255, 0, 127, 0.15);
    }
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background: rgba(10, 10, 10, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        border-left: 3px solid var(--acid-green) !important;
        border-radius: 6px !important;
        font-family: 'Fira Code', monospace !important;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(5, 5, 5, 0.8);
        padding: 8px;
        border-radius: 6px;
        border: 1px solid rgba(0, 240, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: 1px solid transparent;
        border-radius: 4px;
        padding: 10px 20px;
        color: var(--text-dim);
        font-family: 'Fira Code', monospace;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        border: 1px solid var(--electric-cyan) !important;
        color: var(--electric-cyan) !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.3) !important;
    }
    
    /* ===== INPUTS ===== */
    .stSelectbox > div > div, .stTextInput > div > div > input {
        background: rgba(5, 5, 5, 0.9) !important;
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        color: var(--text-bright) !important;
        border-radius: 4px !important;
        font-family: 'Fira Code', monospace !important;
    }
    
    .stSelectbox > div > div:focus-within, .stTextInput > div > div > input:focus {
        border-color: var(--electric-cyan) !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.2) !important;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: var(--void-black); }
    ::-webkit-scrollbar-thumb { 
        background: linear-gradient(180deg, var(--electric-cyan), var(--hot-pink)); 
        border-radius: 4px;
    }
    
    /* ===== STATUS BADGES ===== */
    .badge-secure {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        background: rgba(0, 255, 159, 0.1);
        border: 1px solid var(--acid-green);
        border-radius: 4px;
        color: var(--acid-green);
        font-family: 'Fira Code', monospace;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px var(--acid-green);
        box-shadow: 0 0 15px rgba(0, 255, 159, 0.2);
    }
    
    .badge-alert {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        background: rgba(255, 0, 127, 0.1);
        border: 1px solid var(--hot-pink);
        border-radius: 4px;
        color: var(--hot-pink);
        font-family: 'Fira Code', monospace;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px var(--hot-pink);
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.2);
        animation: alertPulse 2s ease-in-out infinite;
    }
    
    @keyframes alertPulse {
        0%, 100% { box-shadow: 0 0 15px rgba(255, 0, 127, 0.2); }
        50% { box-shadow: 0 0 30px rgba(255, 0, 127, 0.5); }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
@st.cache_data
def load_data(path):
    if os.path.exists(path):
        dp = DataPreprocessor(path)
        df = dp.load_data()
        df = dp.clean_and_encode()
        train_X, test_X, train_y, test_y, train_mal_y, test_mal_y = dp.split_data()
        return dp, df, train_X, test_X, train_y, test_y, train_mal_y, test_mal_y
    return None, None, None, None, None, None, None, None

def save_history(record):
    hf = get_path('scan_history.json')
    history = []
    if os.path.exists(hf):
        with open(hf, 'r') as f:
            try: history = json.load(f)
            except: pass
    history.append(record)
    with open(hf, 'w') as f:
        json.dump(history, f, indent=2)

def load_history():
    hf = get_path('scan_history.json')
    if os.path.exists(hf):
        with open(hf, 'r') as f:
            try: return json.load(f)
            except: return []
    return []

def cyber_metric(value, label, color="#00F0FF"):
    return f'''
    <div class="metric-cyber">
        <div class="metric-value" style="color: {color};">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    '''

# ============================================================================
# SIDEBAR - HACKER'S TERMINAL
# ============================================================================
with st.sidebar:
    # Terminal Header
    st.markdown("""
    <div style="padding: 20px 16px; border-bottom: 1px solid rgba(0, 240, 255, 0.3);">
        <div style="font-family: 'Fira Code'; font-size: 0.7rem; color: #999; margin-bottom: 8px;">root@cybersentinel:~#</div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="font-size: 2.5rem; filter: drop-shadow(0 0 15px rgba(0, 240, 255, 0.5));">🛡️</div>
            <div>
                <div style="font-family: 'Orbitron'; font-size: 1.1rem; font-weight: 700; color: #00F0FF; text-shadow: 0 0 10px #00F0FF; letter-spacing: 3px;">CYBERSENTINEL</div>
                <div style="font-family: 'Fira Code'; font-size: 0.6rem; color: #999; letter-spacing: 2px;">v2.0.0 // MEMORY FORENSICS</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Dataset Input
    default_path = "malmem.csv"
    if not os.path.exists(default_path):
        pp = os.path.join(BASE_DIR, "malmem.csv")
        default_path = pp if os.path.exists(pp) else "../malmem.csv" if os.path.exists("../malmem.csv") else default_path
    
    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-family: Fira Code; font-size: 0.7rem; color: #00F0FF; margin-left: 12px;'>> DATASET_PATH</div>", unsafe_allow_html=True)
    data_path = st.text_input("path", default_path, label_visibility="collapsed")
    
    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-family: Fira Code; font-size: 0.7rem; color: #FF007F; margin-left: 12px; margin-bottom: 8px;'>> COMMAND_DECK</div>", unsafe_allow_html=True)
    
    # Navigation Buttons
    nav = [
        ("dashboard", "📊", "DASHBOARD"),
        ("scan", "🔍", "SCAN_DUMP"),
        ("train", "🧠", "TRAIN_MODELS"),
        ("history", "📜", "HISTORY")
    ]
    
    for key, icon, label in nav:
        is_active = st.session_state.page == key
        btn_style = "cyber-btn active" if is_active else "cyber-btn"
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()
    
    # System Status - Heartbeat
    st.markdown("""
    <div style="margin-top: 40px; padding: 16px;">
        <div style="font-family: 'Fira Code'; font-size: 0.65rem; color: #999; margin-bottom: 8px;">> SYSTEM_STATUS</div>
        <div style="padding: 16px; background: rgba(0, 255, 159, 0.05); border: 1px solid rgba(0, 255, 159, 0.3); border-radius: 6px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div class="heartbeat" style="width: 12px; height: 12px; background: #00FF9F; border-radius: 50%; box-shadow: 0 0 10px #00FF9F, 0 0 20px #00FF9F;"></div>
                <div>
                    <div style="font-family: 'Fira Code'; font-size: 0.8rem; color: #00FF9F; text-shadow: 0 0 5px #00FF9F;">ONLINE</div>
                    <div style="font-family: 'Fira Code'; font-size: 0.6rem; color: #999;">ALL SYSTEMS NOMINAL</div>
                </div>
            </div>
            <div style="margin-top: 12px; font-family: 'Fira Code'; font-size: 0.6rem; color: #777;">
                <div>> CPU: <span style="color: #00F0FF;">OK</span></div>
                <div>> MEM: <span style="color: #00F0FF;">OK</span></div>
                <div>> NET: <span style="color: #00FF9F;">ACTIVE</span></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# LOAD DATA
# ============================================================================
dp, df, X_train, X_test, y_train, y_test, y_mal_train, y_mal_test = load_data(data_path)

if df is None:
    st.markdown("""
    <div class="glass-card" style="text-align: center; max-width: 500px; margin: 100px auto;">
        <div style="font-size: 3rem; margin-bottom: 16px;">⚠️</div>
        <div style="font-family: 'Orbitron'; font-size: 1.2rem; color: #FF007F; margin-bottom: 8px; text-shadow: 0 0 10px #FF007F;">CRITICAL ERROR</div>
        <div style="font-family: 'Fira Code'; color: #888; font-size: 0.85rem;">> dataset_not_found</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

page = st.session_state.page

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
if page == "dashboard":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("# THREAT INTELLIGENCE")
        st.markdown("<p style='font-family: Fira Code; color: #999; font-size: 0.8rem; letter-spacing: 2px;'>> real-time memory forensics analysis</p>", unsafe_allow_html=True)
    with col2:
        mal_ratio = df['Class'].mean() * 100
        if mal_ratio < 50:
            st.markdown('<div style="text-align: right; padding-top: 16px;"><span class="badge-secure">[✓] SECURE</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: right; padding-top: 16px;"><span class="badge-alert">[!] ALERT</span></div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 24px'></div>", unsafe_allow_html=True)
    
    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(cyber_metric(f"{df.shape[0]:,}", "TOTAL_SAMPLES", "#00F0FF"), unsafe_allow_html=True)
    with c2:
        color = "#FF007F" if mal_ratio > 30 else "#00FF9F"
        st.markdown(cyber_metric(f"{mal_ratio:.1f}%", "MALWARE_RATE", color), unsafe_allow_html=True)
    with c3:
        st.markdown(cyber_metric(f"{df.shape[1]-2}", "FEATURES", "#FF007F"), unsafe_allow_html=True)
    with c4:
        st.markdown(cyber_metric(f"{len(load_history())}", "TOTAL_SCANS", "#00FF9F"), unsafe_allow_html=True)
    
    st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
    
    # Charts
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("## 3D_MEMORY_CLUSTERING")
        
        pca = PCA(n_components=3)
        n = min(2000, len(X_train))
        X_pca = pca.fit_transform(X_train.iloc[:n])
        
        viz = pd.DataFrame(X_pca, columns=['PC1', 'PC2', 'PC3'])
        viz['Class'] = y_train.iloc[:n].map({0: 'Benign', 1: 'Malware'}).values
        
        # Neon glowing scatter plot
        fig = px.scatter_3d(viz, x='PC1', y='PC2', z='PC3', color='Class',
            color_discrete_map={'Benign': '#00F0FF', 'Malware': '#FF007F'}, opacity=0.85)
        
        fig.update_traces(marker=dict(size=4, line=dict(width=0)))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#555', family='Fira Code'),
            legend=dict(
                bgcolor='rgba(5,5,5,0.9)', 
                bordercolor='rgba(0,240,255,0.3)', 
                borderwidth=1,
                font=dict(color='#eee', family='Fira Code')
            ),
            scene=dict(
                xaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(0,240,255,0.1)', zerolinecolor='rgba(0,240,255,0.2)', title_font=dict(color='#00F0FF')),
                yaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(0,240,255,0.1)', zerolinecolor='rgba(0,240,255,0.2)', title_font=dict(color='#00F0FF')),
                zaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(0,240,255,0.1)', zerolinecolor='rgba(0,240,255,0.2)', title_font=dict(color='#00F0FF'))
            ),
            margin=dict(l=0, r=0, t=10, b=0), 
            height=480
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.markdown("## CLASS_DISTRIBUTION")
        
        counts = df['Class'].value_counts()
        fig = go.Figure(data=[go.Pie(
            labels=['Benign', 'Malware'], 
            values=[counts.get(0,0), counts.get(1,0)],
            hole=0.7, 
            marker=dict(colors=['#00F0FF', '#FF007F'], line=dict(color='#050505', width=2)),
            textinfo='percent', 
            textfont=dict(color='#eee', size=14, family='Fira Code')
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10), 
            height=220,
            annotations=[dict(text='CLASSES', x=0.5, y=0.5, font=dict(size=11, color='#555', family='Orbitron'), showarrow=False)]
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("## TOP_FEATURES")
        try:
            rf = joblib.load(get_path('models/RandomForest.pkl'))
            fi = pd.DataFrame({'f': X_train.columns, 'i': rf.feature_importances_}).nlargest(6, 'i')
            
            fig = go.Figure(go.Bar(
                x=fi['i'], y=fi['f'], orientation='h',
                marker=dict(color=fi['i'], colorscale=[[0, '#FF007F'], [0.5, '#00F0FF'], [1, '#00FF9F']])
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#888', size=9, family='Fira Code'),
                xaxis=dict(gridcolor='rgba(0,240,255,0.1)', zeroline=False),
                yaxis=dict(gridcolor='rgba(0,240,255,0.1)'),
                margin=dict(l=0, r=0, t=0, b=0), 
                height=220
            )
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.markdown("<div class='glass-card'><span style='color: #999;'>> train models to view</span></div>", unsafe_allow_html=True)

# ============================================================================
# SCAN PAGE
# ============================================================================
elif page == "scan":
    st.markdown("# THREAT_SCANNER")
    st.markdown("<p style='font-family: Fira Code; color: #999; font-size: 0.8rem;'>> upload memory dump for ai-powered analysis</p>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    
    file = st.file_uploader("Upload CSV", type=["csv"])
    
    if file:
        input_df = pd.read_csv(file)
        
        st.markdown("<div style='font-family: Fira Code; color: #FF007F; font-size: 0.8rem; margin: 16px 0 8px 0;'>> PREVIEW</div>", unsafe_allow_html=True)
        st.dataframe(input_df.head(), use_container_width=True)
        
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            scan = st.button("⚡ EXECUTE_SCAN", use_container_width=True)
        
        if scan:
            prog = st.progress(0, "> initializing...")
            
            try:
                prog.progress(20, "> preprocessing data...")
                scan_df = input_df.copy()
                for c in ['Class', 'Category']:
                    if c in scan_df.columns: scan_df = scan_df.drop(columns=[c])
                scan_df = scan_df[X_train.columns]
                scaled = dp.scaler.transform(scan_df)
                
                prog.progress(40, "> loading neural networks...")
                ens = joblib.load(get_path('models/ensemble.pkl'))
                anom = joblib.load(get_path('models/anomaly_detector.pkl'))
                multi = joblib.load(get_path('models/mlp_multiclass.pkl'))
                
                prog.progress(60, "> analyzing patterns...")
                preds = ens.predict(scaled)
                probs = ens.predict_proba(scaled)
                scores = anom.decision_function(scaled)
                
                prog.progress(80, "> classifying threats...")
                
                results = []
                for i, p in enumerate(preds):
                    is_mal = bool(p == 1)
                    mtype = "N/A"
                    if is_mal:
                        idx = multi.predict([scaled[i]])[0]
                        mtype = dp.malware_encoder.inverse_transform([idx])[0]
                    
                    r = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "sample_id": int(i),
                        "status": "Malware" if is_mal else "Benign",
                        "type": str(mtype),
                        "confidence": float(max(probs[i]) * 100),
                        "anomaly_score": float(scores[i]),
                        "is_anomaly": bool(scores[i] < 0)
                    }
                    results.append(r)
                    save_history(r)
                
                prog.progress(100, "> scan complete")
                
                st.markdown("---")
                st.markdown("<div style='font-family: Orbitron; color: #00F0FF; font-size: 1rem; letter-spacing: 2px; margin-bottom: 16px;'>> RESULTS</div>", unsafe_allow_html=True)
                
                mal_c = sum(1 for r in results if r['status'] == 'Malware')
                
                c1, c2, c3, c4 = st.columns(4)
                with c1: st.markdown(cyber_metric(len(results), "SCANNED", "#00F0FF"), unsafe_allow_html=True)
                with c2: st.markdown(cyber_metric(len(results)-mal_c, "BENIGN", "#00FF9F"), unsafe_allow_html=True)
                with c3: st.markdown(cyber_metric(mal_c, "MALWARE", "#FF007F"), unsafe_allow_html=True)
                with c4: st.markdown(cyber_metric(sum(1 for r in results if r['is_anomaly']), "ANOMALIES", "#FFFF00"), unsafe_allow_html=True)
                
                st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
                
                for i, r in enumerate(results):
                    icon = "🔴" if r['status'] == 'Malware' else "🟢"
                    with st.expander(f"{icon} SAMPLE_{i} :: {r['status'].upper()} :: {r['confidence']:.0f}%"):
                        c1, c2, c3 = st.columns(3)
                        c1.metric("> STATUS", r['status'])
                        c2.metric("> CONFIDENCE", f"{r['confidence']:.1f}%")
                        c3.metric("> ANOMALY_SCORE", f"{r['anomaly_score']:.3f}")
                        if r['status'] == 'Malware':
                            st.info(f"🦠 FAMILY: **{r['type']}**")
                
                st.markdown("---")
                gen = ForensicsReportGenerator()
                html, rid = gen.generate_report(results)
                link = gen.get_download_link(html, f"report_{rid}.html")
                
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 8px;">📄</div>
                    <div style="font-family: 'Orbitron'; color: #00F0FF; text-shadow: 0 0 10px #00F0FF;">> REPORT_GENERATED</div>
                    <div style="font-family: 'Fira Code'; color: #999; font-size: 0.8rem; margin: 8px 0;">forensic analysis complete</div>
                    {link}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"> ERROR: {e}")
                st.info("> run TRAIN_MODELS first")

# ============================================================================
# TRAIN PAGE
# ============================================================================
elif page == "train":
    st.markdown("# MODEL_TRAINING")
    st.markdown("<p style='font-family: Fira Code; color: #999; font-size: 0.8rem;'>> initialize and optimize ai detection models</p>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    
    t1, t2, t3 = st.tabs(["⚡ ENSEMBLE", "🧠 NEURAL_NET", "🔍 ANOMALY"])
    
    with t1:
        st.markdown("""<div class="glass-card"><div style="font-family: 'Orbitron'; color: #00F0FF; text-shadow: 0 0 5px #00F0FF;">> SUPER_LEARNER_ENSEMBLE</div><div style="font-family: 'Fira Code'; color: #999; font-size: 0.8rem; margin-top: 4px;">RF + LogReg + MLP combined classifier</div></div>""", unsafe_allow_html=True)
        st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
        if st.button("TRAIN_ENSEMBLE", key="ens"):
            p = st.progress(0, "> initializing...")
            adv = AdvancedModelTrainer(X_train, y_train, X_test, y_test, y_mal_train, y_mal_test)
            p.progress(30, "> training ensemble..."); adv.train_ensemble_model()
            p.progress(60, "> training multiclass..."); adv.train_malware_type_model()
            p.progress(90, "> saving models..."); adv.save_models()
            p.progress(100, "> complete")
            st.success("> ensemble trained successfully")
    
    with t2:
        st.markdown("""<div class="glass-card"><div style="font-family: 'Orbitron'; color: #FF007F; text-shadow: 0 0 5px #FF007F;">> OPTIMIZED_MLP</div><div style="font-family: 'Fira Code'; color: #999; font-size: 0.8rem; margin-top: 4px;">neural network with hyperparameter tuning</div></div>""", unsafe_allow_html=True)
        st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
        if st.button("TRAIN_MLP", key="mlp"):
            with st.spinner("> optimizing neural network..."):
                adv = AdvancedModelTrainer(X_train, y_train, X_test, y_test, y_mal_train, y_mal_test)
                adv.build_and_optimize_mlp()
                adv.save_models()
                st.success("> mlp trained successfully")
    
    with t3:
        st.markdown("""<div class="glass-card"><div style="font-family: 'Orbitron'; color: #00FF9F; text-shadow: 0 0 5px #00FF9F;">> ISOLATION_FOREST</div><div style="font-family: 'Fira Code'; color: #999; font-size: 0.8rem; margin-top: 4px;">detect novel threats & zero-day attacks</div></div>""", unsafe_allow_html=True)
        st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
        if st.button("TRAIN_DETECTOR", key="anom"):
            with st.spinner("> training anomaly detector..."):
                adv = AdvancedModelTrainer(X_train, y_train, X_test, y_test, y_mal_train, y_mal_test)
                adv.train_anomaly_detector()
                adv.save_models()
                st.success("> detector trained successfully")
    
    st.markdown("---")
    st.markdown("<div style='font-family: Orbitron; color: #FF007F; font-size: 0.9rem; letter-spacing: 2px;'>> MODEL_STATUS</div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
    
    models = {"ENSEMBLE": "models/ensemble.pkl", "MULTICLASS": "models/mlp_multiclass.pkl", "MLP": "models/mlp_optimized.pkl", "ANOMALY": "models/anomaly_detector.pkl", "RF": "models/RandomForest.pkl"}
    
    cols = st.columns(len(models))
    for i, (n, p) in enumerate(models.items()):
        with cols[i]:
            ok = os.path.exists(get_path(p))
            color = "#00FF9F" if ok else "#FF007F"
            st.markdown(f"""<div style="text-align: center; padding: 14px; background: rgba(5,5,5,0.8); border-radius: 6px; border: 1px solid {color}; border-left: 3px solid {color};">
                <div style="font-size: 1.2rem; color: {color}; text-shadow: 0 0 10px {color};">{'✓' if ok else '✗'}</div>
                <div style="font-family: 'Fira Code'; font-size: 0.6rem; color: #999; margin-top: 4px;">{n}</div>
            </div>""", unsafe_allow_html=True)

# ============================================================================
# HISTORY PAGE
# ============================================================================
elif page == "history":
    st.markdown("# SCAN_HISTORY")
    st.markdown("<p style='font-family: Fira Code; color: #999; font-size: 0.8rem;'>> previous analysis records</p>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    
    history = load_history()
    
    if history:
        mal = sum(1 for h in history if h.get('status') == 'Malware')
        rate = (mal / len(history) * 100) if history else 0
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(cyber_metric(len(history), "TOTAL_SCANS", "#00F0FF"), unsafe_allow_html=True)
        with c2: st.markdown(cyber_metric(mal, "MALWARE_FOUND", "#FF007F"), unsafe_allow_html=True)
        with c3: st.markdown(cyber_metric(f"{rate:.1f}%", "DETECTION_RATE", "#00FF9F"), unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown("<span style='font-family: Fira Code; color: #999; font-size: 0.75rem;'>> FILTER</span>", unsafe_allow_html=True)
            filt = st.selectbox("filter", ["All", "Malware", "Benign"], label_visibility="collapsed")
        with c2:
            st.markdown("<div style='height: 24px'></div>", unsafe_allow_html=True)
            if st.button("🗑️ CLEAR_ALL"):
                hf = get_path('scan_history.json')
                if os.path.exists(hf): os.remove(hf)
                st.rerun()
        
        filtered = history if filt == "All" else [h for h in history if h.get('status') == filt]
        st.dataframe(pd.DataFrame(filtered), use_container_width=True)
        
        st.markdown("---")
        csv = pd.DataFrame(filtered).to_csv(index=False)
        st.download_button("📥 EXPORT_CSV", csv, "history.csv", "text/csv")
    else:
        st.markdown("<div class='glass-card' style='text-align: center;'><span style='color: #999;'>> no scan history found</span></div>", unsafe_allow_html=True)
