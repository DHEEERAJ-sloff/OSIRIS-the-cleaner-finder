# OSIRIS Demo Launcher (PowerShell)
# RIGHT-CLICK this file -> "Run with PowerShell"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  OSIRIS Forensic Workstation - Demo Launcher" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Install dependencies
Write-Host "[1/3] Installing Python dependencies..." -ForegroundColor Yellow
python -m pip install -r requirements.txt --quiet --disable-pip-version-check
Write-Host "       Done." -ForegroundColor Green
Write-Host ""

# Step 2: Reset demo environment
Write-Host "[2/3] Setting up demo environment..." -ForegroundColor Yellow
python demo_setup.py
Write-Host ""

# Step 3: Launch Streamlit + open browser
Write-Host "[3/3] Launching OSIRIS..." -ForegroundColor Yellow
Write-Host ""
Write-Host "  >>> Browser will open at http://localhost:8501 <<<" -ForegroundColor Green
Write-Host "  Press Ctrl+C to stop the server when done." -ForegroundColor Gray
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Follow DEMO_GUIDE.md step by step" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Open browser after a short delay
Start-Job { Start-Sleep 4; Start-Process "http://localhost:8501" } | Out-Null

# Start Streamlit
python -m streamlit run src/app.py

Write-Host ""
Write-Host "Server stopped. Press any key to close." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
