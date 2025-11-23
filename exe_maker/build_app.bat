@echo off
setlocal

:: ---------------------------------------------------------
:: STEP 0: FIX WORKING DIRECTORY (CRITICAL FIX)
:: When running as Admin, Windows starts in System32.
:: We must switch back to the folder where this script lives.
:: ---------------------------------------------------------
cd /d "%~dp0"

:: ---------------------------------------------------------
:: STEP 1: CHECK FOR ADMINISTRATOR PRIVILEGES
:: ---------------------------------------------------------
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [SUCCESS] Admin rights detected.
) else (
    echo.
    echo ========================================================
    echo                 CRITICAL ERROR: ACCESS DENIED
    echo ========================================================
    echo You are attempting to write to C:\Program Files.
    echo.
    echo You MUST right-click this file and select:
    echo "Run as Administrator"
    echo ========================================================
    echo.
    pause
    exit
)

:: ---------------------------------------------------------
:: STEP 2: INSTALL PYINSTALLER
:: ---------------------------------------------------------
echo.
echo [1/4] Checking and Installing PyInstaller...
pip install pyinstaller
if %errorLevel% neq 0 (
    echo Error installing PyInstaller. Check your internet connection.
    pause
    exit
)

:: ---------------------------------------------------------
:: STEP 3: CREATE THE TARGET DIRECTORY
:: ---------------------------------------------------------
set "TARGET_DIR=C:\Program Files\File Organizer"
echo.
echo [2/4] Creating directory: "%TARGET_DIR%"

if not exist "%TARGET_DIR%" (
    mkdir "%TARGET_DIR%"
)

:: ---------------------------------------------------------
:: STEP 4: RUN PYINSTALLER
:: ---------------------------------------------------------
echo.
echo [3/4] Building the Executable...
echo. 
echo Note: You may see a yellow 'Deprecation' warning. 
echo This is normal when writing to Program Files.
echo.

:: We run PyInstaller from the CURRENT folder ("%~dp0"), 
:: but we tell it to output files to TARGET_DIR.

pyinstaller --noconsole --onefile --name "FileOrganizer" ^
--distpath "%TARGET_DIR%\dist" ^
--workpath "%TARGET_DIR%\build" ^
--specpath "%TARGET_DIR%" ^
"organizer.py"

if %errorLevel% neq 0 (
    echo.
    echo [ERROR] Build failed.
    echo 1. Make sure 'organizer.py' is in this same folder.
    echo 2. If PyInstaller blocked the build due to Admin rights, 
    echo    try changing the TARGET_DIR to your Desktop instead.
    pause
    exit
)

:: ---------------------------------------------------------
:: FINISH
:: ---------------------------------------------------------
echo.
echo ========================================================
echo                 BUILD COMPLETE
echo ========================================================
echo Your app has been created in:
echo "%TARGET_DIR%\dist"
echo.
echo Opening folder now...
explorer "%TARGET_DIR%\dist"
pause