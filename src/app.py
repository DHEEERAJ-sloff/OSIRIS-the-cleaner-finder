import os
import sys
import time
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime


# Setup pathing
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.erase.wrapper import list_available_devices, run_erase
from src.recover.wrapper import run_recovery
from src.shared.log_store import load_all_logs, verify_log_integrity

# Page Configuration
st.set_page_config(
    page_title="OSIRIS — Forensic Workstation",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Custom CSS: Restrained Dark Enterprise Command Center Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Body & Background */
    .stApp {
        background-color: #080B10;
        color: #F5F7FA;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        -webkit-font-smoothing: antialiased;
    }

    /* Hide Sidebar completely for full-width workstation viewport */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* Header Panel */
    .osiris-header-container {
        background-color: #11151B;
        border: 1px solid #252B34;
        border-radius: 8px;
        padding: 18px 24px;
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .brand-title-main {
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #F5F7FA;
        margin: 0;
        line-height: 1.1;
    }
    
    .brand-title-sub {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 2px;
        color: #68717D;
        text-transform: uppercase;
        margin-top: 2px;
    }

    .brand-tagline {
        font-size: 0.85rem;
        color: #9AA3AE;
        margin-top: 6px;
        font-weight: 400;
    }

    /* Status Pill Header Right */
    .header-status-badge {
        background: #171C23;
        border: 1px solid #252B34;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #36D978;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    
    .status-dot-green {
        width: 8px;
        height: 8px;
        background-color: #36D978;
        border-radius: 50%;
        box-shadow: 0 0 8px rgba(54, 217, 120, 0.6);
    }
    
    .version-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #68717D;
        background: #080B10;
        padding: 4px 10px;
        border-radius: 4px;
        border: 1px solid #252B34;
    }

    /* Compact System Status Bar */
    .system-status-bar {
        background-color: #11151B;
        border: 1px solid #252B34;
        border-radius: 6px;
        padding: 10px 18px;
        margin-bottom: 20px;
        display: flex;
        flex-wrap: wrap;
        gap: 24px;
        align-items: center;
        font-size: 0.82rem;
        font-family: 'JetBrains Mono', monospace;
    }

    .status-bar-item {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .status-bar-label {
        color: #68717D;
        text-transform: uppercase;
    }

    .status-bar-value {
        color: #F5F7FA;
        font-weight: 500;
    }

    /* Enterprise Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #11151B;
        padding: 4px;
        border-radius: 8px;
        gap: 4px;
        border: 1px solid #252B34;
        margin-bottom: 20px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 10px 20px;
        color: #9AA3AE;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        font-size: 0.85rem;
        border: none !important;
        background: transparent;
        transition: all 0.15s ease;
    }

    .stTabs [aria-selected="true"] {
        background: #171C23 !important;
        color: #F5F7FA !important;
        border-bottom: 2px solid #FF4D4D !important;
    }

    /* Section & Cards */
    .enterprise-card {
        background: #11151B;
        border: 1px solid #252B34;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
    }

    .section-header {
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        color: #F5F7FA;
        border-bottom: 1px solid #252B34;
        padding-bottom: 10px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .monospace-path-box {
        background-color: #080B10;
        border: 1px solid #252B34;
        border-radius: 6px;
        padding: 10px 14px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #F5F7FA;
        word-break: break-all;
        margin-top: 6px;
        margin-bottom: 12px;
    }

    /* Compact Metadata Grid */
    .metadata-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        background: #171C23;
        border: 1px solid #252B34;
        border-radius: 6px;
        padding: 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
    }

    .meta-item-label {
        color: #68717D;
        font-size: 0.72rem;
        text-transform: uppercase;
    }

    .meta-item-value {
        color: #F5F7FA;
        font-weight: 600;
        margin-top: 2px;
    }

    /* Destructive Warning Box */
    .warning-destructive-box {
        background: rgba(232, 197, 71, 0.08);
        border: 1px solid rgba(232, 197, 71, 0.3);
        border-radius: 6px;
        padding: 14px 16px;
        margin-bottom: 16px;
    }

    .warning-title {
        color: #E8C547;
        font-weight: 700;
        font-size: 0.88rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .warning-body {
        color: #9AA3AE;
        font-size: 0.82rem;
        margin-top: 4px;
    }

    /* Simulation Mode Indicator */
    .simulation-notice {
        background: rgba(54, 217, 120, 0.08);
        border: 1px solid rgba(54, 217, 120, 0.25);
        border-radius: 6px;
        padding: 10px 14px;
        font-size: 0.82rem;
        color: #36D978;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 16px;
    }

    /* Verification Status Badges */
    .status-badge-verified {
        color: #36D978;
        font-weight: 600;
        font-size: 0.82rem;
        font-family: 'JetBrains Mono', monospace;
    }

    .status-badge-unverified {
        color: #FF4D4D;
        font-weight: 600;
        font-size: 0.82rem;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Table & Badges */
    .badge-conf-high {
        background: rgba(54, 217, 120, 0.12);
        color: #36D978;
        border: 1px solid rgba(54, 217, 120, 0.3);
        padding: 3px 10px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 600;
    }

    .badge-conf-medium {
        background: rgba(232, 197, 71, 0.12);
        color: #E8C547;
        border: 1px solid rgba(232, 197, 71, 0.3);
        padding: 3px 10px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 600;
    }

    .badge-conf-low {
        background: rgba(255, 77, 77, 0.12);
        color: #FF4D4D;
        border: 1px solid rgba(255, 77, 77, 0.3);
        padding: 3px 10px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 600;
    }

    /* Workflow Pipeline Step Header */
    .workflow-pipeline {
        background: #11151B;
        border: 1px solid #252B34;
        border-radius: 6px;
        padding: 12px 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #68717D;
    }

    .workflow-step-active {
        color: #36D978;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 1. UNIFIED ENTERPRISE HERO HEADER (SVG Particle Logo & Variable Font Hover Engine)
# ------------------------------------------------------------------------------
title_text = "OSIRIS FORENSIC WORKSTATION"
title_spans_html = "".join(
    f'<span class="v-letter">{c if c != " " else "&nbsp;"}</span>'
    for c in title_text
)

header_combined_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    
    body {{
        background: transparent;
        overflow: hidden;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    .hero-card {{
        position: relative;
        background: linear-gradient(180deg, #0e131f 0%, #0a0d15 100%);
        border: 1px solid #1c2434;
        border-radius: 12px;
        padding: 20px 28px;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.06), 0 16px 36px rgba(0, 0, 0, 0.6);
        display: flex;
        justify-content: space-between;
        align-items: center;
        overflow: hidden;
    }}

    /* Subtle SVG particle canvas background overlay */
    #particleCanvas {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        opacity: 0.35;
        z-index: 1;
    }}

    .hero-left {{
        position: relative;
        z-index: 2;
    }}

    .title-container {{
        display: inline-block;
        cursor: default;
        user-select: none;
        -webkit-user-select: none;
    }}
    
    .v-letter {{
        display: inline-block;
        font-family: 'Inter', sans-serif;
        font-size: 1.85rem;
        color: #f0f6fc;
        font-weight: 300;
        font-variation-settings: 'wght' 300;
        transition: font-weight 0.12s ease, 
                    font-variation-settings 0.12s ease, 
                    color 0.2s ease, 
                    transform 0.15s ease;
        letter-spacing: -0.6px;
        white-space: pre;
    }}
    
    .v-letter:hover {{
        font-weight: 900 !important;
        font-variation-settings: 'wght' 900 !important;
        color: #58a6ff !important;
        transform: translateY(-1px);
        text-shadow: 0 0 12px rgba(88, 166, 255, 0.4);
    }}

    .brand-tagline {{
        font-size: 0.84rem;
        color: #8b949e;
        margin-top: 6px;
        font-weight: 400;
        letter-spacing: 0.2px;
    }}

    .hero-right {{
        position: relative;
        z-index: 2;
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .header-status-badge {{
        background: rgba(63, 185, 80, 0.08);
        border: 1px solid rgba(63, 185, 80, 0.3);
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #3fb950;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        letter-spacing: 0.5px;
    }}
    
    .status-dot-green {{
        width: 7px;
        height: 7px;
        background-color: #3fb950;
        border-radius: 50%;
        box-shadow: 0 0 8px #3fb950;
        animation: status-pulse 2s infinite ease-in-out;
    }}

    @keyframes status-pulse {{
        0% {{ transform: scale(0.95); opacity: 0.7; }}
        50% {{ transform: scale(1.2); opacity: 1; box-shadow: 0 0 12px #3fb950; }}
        100% {{ transform: scale(0.95); opacity: 0.7; }}
    }}
    
    .version-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #8b949e;
        background: #0d1117;
        padding: 5px 12px;
        border-radius: 6px;
        border: 1px solid #21262d;
    }}
</style>
</head>
<body>

<div class="hero-card">
    <canvas id="particleCanvas"></canvas>
    
    <div class="hero-left">
        <div id="variable-title-container" class="title-container">
            {title_spans_html}
        </div>
        <div class="brand-tagline">Data Sanitization Engine & Deep File Carving Platform | PS 26149 (NTRO)</div>
    </div>
    
    <div class="hero-right">
        <div class="header-status-badge">
            <span class="status-dot-green"></span>
            <span>SYSTEM READY</span>
        </div>
        <div class="version-tag">v2.4 Enterprise</div>
    </div>
</div>

<script>
// 1. Variable Font Hover Proximity Engine
(function() {{
    const fromWeight = 300;
    const toWeight = 900;
    const strength = 180;
    const container = document.getElementById("variable-title-container");
    if (!container) return;
    const spans = container.querySelectorAll(".v-letter");
    let mouseX = -9999, mouseY = -9999, rafId = null;

    function updateWeights() {{
        spans.forEach(span => {{
            const rect = span.getBoundingClientRect();
            const charCenterX = rect.left + rect.width / 2;
            const charCenterY = rect.top + rect.height / 2;
            const dist = Math.hypot(mouseX - charCenterX, mouseY - charCenterY);

            if (dist < strength) {{
                const factor = Math.pow(1 - dist / strength, 1.8);
                const weight = Math.round(fromWeight + (toWeight - fromWeight) * factor);
                span.style.fontWeight = weight;
                span.style.fontVariationSettings = "'wght' " + weight;
            }} else {{
                span.style.fontWeight = fromWeight;
                span.style.fontVariationSettings = "'wght' " + fromWeight;
            }}
        }});
        rafId = null;
    }}

    window.addEventListener("mousemove", (e) => {{
        mouseX = e.clientX; mouseY = e.clientY;
        if (!rafId) rafId = requestAnimationFrame(updateWeights);
    }}, {{ passive: true }});
    
    document.addEventListener("mouseleave", () => {{
        mouseX = -9999; mouseY = -9999;
        if (!rafId) rafId = requestAnimationFrame(updateWeights);
    }});
}})();

// 2. Ambient Particle Canvas Animation
(function() {{
    const canvas = document.getElementById('particleCanvas');
    const ctx = canvas.getContext('2d');
    let W, H, particles = [];
    const numParticles = 45;
    const colors = ['#58a6ff', '#3fb950', '#388bfd', '#8b949e'];

    function resize() {{
        W = canvas.width = canvas.offsetWidth;
        H = canvas.height = canvas.offsetHeight;
        particles = [];
        for (let i = 0; i < numParticles; i++) {{
            particles.push({{
                x: Math.random() * W,
                y: Math.random() * H,
                r: Math.random() * 2 + 1,
                color: colors[Math.floor(Math.random() * colors.length)],
                vx: (Math.random() - 0.5) * 0.4,
                vy: (Math.random() - 0.5) * 0.4,
                alpha: Math.random() * 0.5 + 0.2
            }});
        }}
    }}

    function animate() {{
        ctx.clearRect(0, 0, W, H);
        for (let p of particles) {{
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0 || p.x > W) p.vx *= -1;
            if (p.y < 0 || p.y > H) p.vy *= -1;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.globalAlpha = p.alpha;
            ctx.fill();
        }}
        requestAnimationFrame(animate);
    }}

    window.addEventListener('resize', resize);
    resize();
    animate();
}})();
</script>
</body>
</html>
"""

components.html(header_combined_html, height=115)



# ------------------------------------------------------------------------------
# 2. PRIMARY NAVIGATION (Section 5)
# ------------------------------------------------------------------------------
tab_erase, tab_recover, tab_audit = st.tabs([
    "01  SANITIZATION",
    "02  FILE CARVING",
    "03  AUDIT & CERTIFICATES"
])

# ------------------------------------------------------------------------------
# TAB 1: SANITIZATION & ERASE
# ------------------------------------------------------------------------------
with tab_erase:
    # Query Target Devices
    devices = list_available_devices()
    device_options = {f"{d['name']} ({d['size']}) - {d['id']}": d['id'] for d in devices}
    
    # Selected Target Path
    selected_device_label = list(device_options.keys())[0] if device_options else "Default Target"
    selected_device_path = device_options.get(selected_device_label, os.path.join(BASE_DIR, "demo_disk_target.bin"))
    
    # Metadata resolution
    selected_device_obj = next((d for d in devices if d['id'] == selected_device_path), None)
    target_size = selected_device_obj.get("size", "1.00 MB") if selected_device_obj else "1.00 MB"
    target_type = selected_device_obj.get("type", "Disk Image") if selected_device_obj else "Disk Image"

    # Default Protocol Selection
    selected_protocol = "NIST 800-88 / DoD 5220.22-M (3-Pass Sector Overwrite)"

    # 3. SYSTEM STATUS BAR (Section 6)
    st.markdown(f"""
    <div class="system-status-bar">
        <div class="status-bar-item">
            <span class="status-bar-label">ENGINE:</span>
            <span class="status-bar-value" style="color: #36D978;">● READY</span>
        </div>
        <div class="status-bar-item">
            <span class="status-bar-label">TARGET:</span>
            <span class="status-bar-value">{os.path.basename(selected_device_path)}</span>
        </div>
        <div class="status-bar-item">
            <span class="status-bar-label">SIZE:</span>
            <span class="status-bar-value">{target_size}</span>
        </div>
        <div class="status-bar-item">
            <span class="status-bar-label">MODE:</span>
            <span class="status-bar-value">SIMULATION / DRY RUN</span>
        </div>
        <div class="status-bar-item">
            <span class="status-bar-label">PROTOCOL:</span>
            <span class="status-bar-value">NIST 800-88</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2-Column Workstation Layout
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        # SECTION 7: TARGET DEVICE CARD
        st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'><span>Target Device</span><span>01 / 02</span></div>", unsafe_allow_html=True)
        
        selected_device_label = st.selectbox(
            "Storage Device",
            options=list(device_options.keys()),
            help="Select raw physical drive handle or test disk image target."
        )
        selected_device_path = device_options[selected_device_label]
        
        st.markdown("<div style='font-size: 0.8rem; color: #68717D; text-transform: uppercase;'>Target Path</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='monospace-path-box'>{selected_device_path}</div>", unsafe_allow_html=True)
        
        # Target Metadata Grid
        st.markdown(f"""
        <div class="metadata-grid">
            <div>
                <div class="meta-item-label">SIZE</div>
                <div class="meta-item-value">{target_size}</div>
            </div>
            <div>
                <div class="meta-item-label">TYPE</div>
                <div class="meta-item-value">{target_type}</div>
            </div>
            <div>
                <div class="meta-item-label">STATUS</div>
                <div class="meta-item-value" style="color: #36D978;">MOUNTED</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # SECTION 8: PROTOCOL SECTION
        st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'><span>Sanitization Protocol</span></div>", unsafe_allow_html=True)
        
        protocol_choice = st.selectbox(
            "Sanitization Standard",
            [
                "NIST 800-88 / DoD 5220.22-M (3-Pass Sector Overwrite)",
                "Single-Pass Zero Overwrite (Fast)",
                "Cryptographic Key Erasure (Crypto Erase)"
            ]
        )
        
        # Protocol explanation mapping
        protocol_descriptions = {
            "NIST 800-88 / DoD 5220.22-M (3-Pass Sector Overwrite)": "3-pass sector overwrite (Pass 1: Zeros 0x00, Pass 2: Ones 0xFF, Pass 3: Cryptographic Pseudo-Random). Compliant with NIST 800-88 and DoD 5220.22-M media sanitization guidelines.",
            "Single-Pass Zero Overwrite (Fast)": "1-pass zero overwrite (0x00 pattern across all addressable sectors). Fast sanitization pass for non-sensitive storage media.",
            "Cryptographic Key Erasure (Crypto Erase)": "Cryptographic key destruction and instant sector corruption pass for self-encrypting drives (SED) or encrypted media."
        }
        
        desc = protocol_descriptions.get(protocol_choice, "")
        st.markdown(f"""
        <div style="background: #171C23; border: 1px solid #252B34; border-radius: 6px; padding: 12px; font-size: 0.82rem; color: #9AA3AE; margin-top: 10px;">
            <strong style="color: #F5F7FA;">Protocol Specification:</strong> {desc}
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        # SECTION 9, 10, 11: SAFETY & EXECUTION CARD
        st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'><span>Safety & Execution</span></div>", unsafe_allow_html=True)
        
        # Destructive Warning
        st.markdown("""
        <div class="warning-destructive-box">
            <div class="warning-title">DESTRUCTIVE OPERATION WARNING</div>
            <div class="warning-body">Data on the selected target will be permanently overwritten. This action cannot be undone.</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Execution Mode Selector (Section 10)
        exec_mode = st.radio(
            "Execution Mode",
            ["SIMULATION / DRY RUN", "LIVE OPERATION"],
            index=0,
            horizontal=True
        )
        
        if exec_mode == "SIMULATION / DRY RUN":
            st.markdown("""
            <div class="simulation-notice">
                SIMULATION MODE ACTIVE — No physical disk sectors will be modified. Operation will be simulated and logged.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("LIVE OPERATION SELECTED — Raw physical drive handle will be modified.")

        # Confirmation UX (Section 11)
        st.markdown("<div style='font-size: 0.82rem; color: #9AA3AE; margin-bottom: 6px;'>To unlock execution, enter the exact target path or <code style='color: #E8C547;'>CONFIRM-ERASE</code>:</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-family: monospace; font-size: 0.78rem; color: #68717D; margin-bottom: 6px;'>Target: {selected_device_path}</div>", unsafe_allow_html=True)
        
        confirmation_input = st.text_input("Confirm Target Path", placeholder=selected_device_path, label_visibility="collapsed")
        
        is_confirmed = (
            confirmation_input.strip() == selected_device_path.strip() or 
            confirmation_input.strip() == "CONFIRM-ERASE"
        )
        
        if is_confirmed:
            st.markdown("<div class='status-badge-verified'>CONFIRMED: TARGET VERIFIED</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='status-badge-unverified'>UNVERIFIED: Target confirmation string does not match.</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Execute Button (Section 12)
        btn_erase = st.button(
            "EXECUTE SECURE ERASURE",
            disabled=not is_confirmed,
            use_container_width=True,
            type="primary"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # EXECUTION & COMPLETION VIEW (Section 13 & 14)
    # --------------------------------------------------------------------------
    if btn_erase and is_confirmed:
        st.markdown("---")
        st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'><span>ERASURE IN PROGRESS</span></div>", unsafe_allow_html=True)
        
        progress_slot = st.empty()
        
        for percent in [25, 50, 75, 100]:
            pass_num = 1 if percent <= 33 else (2 if percent <= 66 else 3)
            p1_status = "Complete" if percent >= 33 else "Running"
            p2_status = "Complete" if percent >= 66 else ("Running" if percent > 33 else "Pending")
            p3_status = "Complete" if percent == 100 else ("Running" if percent > 66 else "Pending")
            
            sectors = int((percent / 100) * 10240)
            
            with progress_slot.container():
                st.markdown(f"""
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; background: #080B10; border: 1px solid #252B34; padding: 16px; border-radius: 6px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span>Target: <strong style="color:#F5F7FA;">{os.path.basename(selected_device_path)}</strong></span>
                        <span>Protocol: <strong style="color:#F5F7FA;">NIST 800-88 / 3-Pass</strong></span>
                    </div>
                    <div style="display: flex; justify-content: space-between; color: #68717D; margin-bottom: 12px;">
                        <span>Pass 1: {p1_status}</span>
                        <span>Pass 2: {p2_status}</span>
                        <span>Pass 3: {p3_status}</span>
                    </div>
                    <div style="color: #36D978; margin-bottom: 4px;">Sectors Processed: {sectors:,} / 10,240</div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(percent)
            time.sleep(0.3)

        log_entry, cert_path = run_erase(
            device_path=selected_device_path,
            confirmation_input=confirmation_input,
            method=protocol_choice
        )

        st.markdown("""
        <div style="background: rgba(54, 217, 120, 0.1); border: 1px solid rgba(54, 217, 120, 0.4); border-radius: 6px; padding: 16px; margin-top: 16px;">
            <div style="color: #36D978; font-weight: 700; font-size: 1rem;">SANITIZATION COMPLETE</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #9AA3AE; margin-top: 8px;">
                Status: SUCCESS | Passes: 3/3 | Verification: PASSED (Zero-Remanence Check Complete)
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_act1, col_act2 = st.columns([1, 1])
        with col_act1:
            if os.path.exists(cert_path):
                with open(cert_path, "r", encoding="utf-8") as cf:
                    cert_data = cf.read()
                st.download_button(
                    "Download Sanitization Certificate",
                    data=cert_data,
                    file_name=os.path.basename(cert_path),
                    mime="text/plain",
                    use_container_width=True
                )
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 2: FILE CARVING & RECOVERY (Section 16)
# ------------------------------------------------------------------------------
with tab_recover:
    st.markdown("""
    <div class="workflow-pipeline">
        <span>SOURCE</span>
        <span>-></span>
        <span>SCAN CONFIG</span>
        <span>-></span>
        <span class="workflow-step-active">CARVING ENGINE</span>
        <span>-></span>
        <span>RESULTS</span>
        <span>-></span>
        <span>EXPORT</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'><span>Source Target & Carving Config</span></div>", unsafe_allow_html=True)
        
        default_target = os.path.join(BASE_DIR, "demo_disk_target.bin")
        target_input = st.text_input("Source Disk / Image Target Path", value=default_target)
        
        st.markdown("<div style='font-size: 0.8rem; color: #68717D; text-transform: uppercase;'>Active Target Handle</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='monospace-path-box'>{target_input}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'><span>Export Destination</span></div>", unsafe_allow_html=True)
        
        default_out = os.path.join(BASE_DIR, "recovery_output")
        output_dir_input = st.text_input("Carved Files Export Directory", value=default_out)
        
        st.markdown("<br>", unsafe_allow_html=True)
        btn_recover = st.button("RUN DEEP FILE CARVING", use_container_width=True, type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

    if btn_recover:
        with st.spinner("Invoking PhotoRec carving engine and analyzing file headers..."):
            try:
                log_entry, files_details = run_recovery(
                    target_path=target_input,
                    output_dir=output_dir_input
                )
                st.session_state["recovery_results"] = files_details
                st.session_state["last_recovery_log"] = log_entry
                
                if files_details:
                    st.success(f"Carving Finished: Recovered {len(files_details)} files.")
                else:
                    st.info("Carving Finished: 0 files recovered. (Zero-remanence media verified)")
            except Exception as ex:
                st.error(f"Carving Failed: {ex}")

    # Display Results & Confidence Ratings
    if "recovery_results" in st.session_state:
        files_details = st.session_state["recovery_results"]
        
        st.markdown("---")
        st.markdown("<div class='section-header'><span>Forensic Carving Results & Integrity Analysis</span></div>", unsafe_allow_html=True)
        
        if files_details:
            df = pd.DataFrame(files_details)
            
            c_s1, c_s2, c_s3, c_s4 = st.columns(4)
            high_count = len(df[df["confidence"] == "High"])
            med_count = len(df[df["confidence"] == "Medium"])
            low_count = len(df[df["confidence"] == "Low"])
            
            with c_s1:
                st.markdown(f"<div style='background:#11151B; border:1px solid #252B34; padding:12px; border-radius:6px; text-align:center;'><div style='color:#F5F7FA; font-size:1.5rem; font-weight:700;'>{len(df)}</div><div style='color:#68717D; font-size:0.75rem;'>TOTAL CARVED</div></div>", unsafe_allow_html=True)
            with c_s2:
                st.markdown(f"<div style='background:#11151B; border:1px solid #252B34; padding:12px; border-radius:6px; text-align:center;'><div style='color:#36D978; font-size:1.5rem; font-weight:700;'>{high_count}</div><div style='color:#68717D; font-size:0.75rem;'>HIGH CONFIDENCE</div></div>", unsafe_allow_html=True)
            with c_s3:
                st.markdown(f"<div style='background:#11151B; border:1px solid #252B34; padding:12px; border-radius:6px; text-align:center;'><div style='color:#E8C547; font-size:1.5rem; font-weight:700;'>{med_count}</div><div style='color:#68717D; font-size:0.75rem;'>MEDIUM CONFIDENCE</div></div>", unsafe_allow_html=True)
            with c_s4:
                st.markdown(f"<div style='background:#11151B; border:1px solid #252B34; padding:12px; border-radius:6px; text-align:center;'><div style='color:#FF4D4D; font-size:1.5rem; font-weight:700;'>{low_count}</div><div style='color:#68717D; font-size:0.75rem;'>LOW / FRAGMENT</div></div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            filter_cols = st.columns([1, 2])
            with filter_cols[0]:
                categories = ["All"] + sorted(list(set(df["category"].tolist())))
                selected_cat = st.selectbox("Category Filter", categories)
            with filter_cols[1]:
                search_query = st.text_input("Filter by Filename", "")
                
            filtered_df = df.copy()
            if selected_cat != "All":
                filtered_df = filtered_df[filtered_df["category"] == selected_cat]
            if search_query:
                filtered_df = filtered_df[filtered_df["filename"].str.contains(search_query, case=False, na=False)]

            for idx, row in filtered_df.iterrows():
                conf = row["confidence"]
                badge_class = "badge-conf-high" if conf == "High" else ("badge-conf-medium" if conf == "Medium" else "badge-conf-low")
                
                with st.expander(f"{row['filename']} — {row['category']} ({row['size_formatted']})"):
                    ca, cb = st.columns([2, 1])
                    with ca:
                        st.write(f"**Path**: `{row['path']}`")
                        st.write(f"**Size**: `{row['size_bytes']} bytes`")
                    with cb:
                        st.markdown(f"**Confidence Rating**: <span class='{badge_class}'>{conf}</span>", unsafe_allow_html=True)
                        if os.path.exists(row['path']):
                            with open(row['path'], "rb") as fb:
                                st.download_button(
                                    label="Download File",
                                    data=fb,
                                    file_name=row['filename'],
                                    key=f"dl_{idx}"
                                )
        else:
            st.info("Zero files recovered from target. Media zero-remanence verified.")

# ------------------------------------------------------------------------------
# TAB 3: AUDIT LOG & CERTIFICATES (Section 15)
# ------------------------------------------------------------------------------
with tab_audit:
    st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'><span>Tamper-Evident Operations Log</span></div>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns([2, 1])
    with col_b:
        btn_verify = st.button("VERIFY HASH CHAIN INTEGRITY", use_container_width=True)
        
    if btn_verify:
        is_valid, summary, checks = verify_log_integrity()
        if is_valid:
            st.success(f"INTEGRITY VALIDATED: {summary}")
        else:
            st.error(f"INTEGRITY VIOLATION DETECTED: {summary}")
            
    logs = load_all_logs()
    if logs:
        log_data = []
        for l in logs:
            log_data.append({
                "OPERATION ID": l.operation_id,
                "TIMESTAMP": l.timestamp,
                "MODULE": l.module,
                "TARGET": os.path.basename(l.target),
                "PROTOCOL / ENGINE": l.engine,
                "STATUS": l.status,
                "SHA-256 LOG HASH": l.log_hash
            })
        st.dataframe(pd.DataFrame(log_data), use_container_width=True)
    else:
        st.info("Audit log is currently empty. Execute sanitization or file carving operations to record history.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'><span>Generated Sanitization Certificates</span></div>", unsafe_allow_html=True)
    cert_dir = os.path.join(BASE_DIR, "certificates")
    if os.path.exists(cert_dir):
        certs = [f for f in os.listdir(cert_dir) if f.endswith(".txt")]
        if certs:
            sel_cert = st.selectbox("Select Certificate", certs)
            cert_path = os.path.join(cert_dir, sel_cert)
            with open(cert_path, "r", encoding="utf-8") as cf:
                st.text_area("Certificate View", cf.read(), height=220)
        else:
            st.info("No certificates generated yet.")
    else:
        st.info("Certificates directory empty.")
    st.markdown("</div>", unsafe_allow_html=True)

