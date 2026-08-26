@echo off
:: Launches the PowerShell demo script with execution policy bypass
:: This works even on OneDrive / restricted Windows machines
powershell -ExecutionPolicy Bypass -NoExit -File "%~dp0start_demo.ps1"
