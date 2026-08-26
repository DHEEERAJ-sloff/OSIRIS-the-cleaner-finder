#!/bin/bash
# ============================================================
#  OSIRIS — Demo Launcher (Linux / macOS)
#  Run: bash start_demo.sh
#  No configuration needed — works on any machine.
# ============================================================

# Move to the directory where this script lives
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "============================================================"
echo "  OSIRIS Forensic Workstation — Demo Launcher"
echo "============================================================"
echo ""

# Check Python
if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo "[ERROR] Python 3 is not installed or not on your PATH."
    echo "        Install Python 3.10+ from https://python.org"
    exit 1
fi

# Use python3 if available, else python
PYTHON=$(command -v python3 || command -v python)

# Install dependencies
echo "[1/3] Checking Python dependencies..."
"$PYTHON" -m pip install -r requirements.txt --quiet --disable-pip-version-check
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies."
    exit 1
fi
echo "       OK — all packages ready."
echo ""

# Run demo setup
echo "[2/3] Resetting demo environment (creating files, clearing logs)..."
"$PYTHON" demo_setup.py
if [ $? -ne 0 ]; then
    echo "[ERROR] demo_setup.py failed."
    exit 1
fi
echo ""

# Launch Streamlit
echo "[3/3] Launching OSIRIS Dashboard..."
echo "       Browser will open at http://localhost:8501"
echo "       (Ctrl+C to stop the server)"
echo ""
echo "============================================================"
echo "  DEMO READY — Follow DEMO_GUIDE.md for step-by-step flow"
echo "============================================================"
echo ""

"$PYTHON" -m streamlit run src/app.py
