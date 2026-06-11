@echo off
rem Nightly Opp Day minutes refresh — reads vault reports, rebuilds JSON, pushes.
rem Registered in Windows Task Scheduler as IS1-OppDay-Minutes-Refresh (21:45 daily).
cd /d "%~dp0.."
echo. >> "%LOCALAPPDATA%\oppday_refresh.log"
echo ===== %date% %time% ===== >> "%LOCALAPPDATA%\oppday_refresh.log"
python scripts\build_oppday_minutes.py --push >> "%LOCALAPPDATA%\oppday_refresh.log" 2>&1
