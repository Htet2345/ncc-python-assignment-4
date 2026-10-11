$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
# Keep temporary installation files inside the project.
New-Item -ItemType Directory -Path '.tmp' -Force | Out-Null
$env:TEMP = Join-Path $PSScriptRoot '.tmp'
$env:TMP = $env:TEMP
if (-not (Test-Path '.venv/Scripts/python.exe')) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Could not create the virtual environment. Install Python 3.10 or later.' }
}
& '.venv/Scripts/python.exe' -m ensurepip --upgrade
if ($LASTEXITCODE -ne 0) { throw 'Could not initialize pip.' }
& '.venv/Scripts/python.exe' -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed. Check your internet connection.' }
& '.venv/Scripts/python.exe' manage.py migrate
if ($LASTEXITCODE -ne 0) { throw 'Database setup failed.' }
& '.venv/Scripts/python.exe' manage.py check
if ($LASTEXITCODE -ne 0) { throw 'Django checks failed.' }
Write-Host 'Setup complete. Run the Django: Run server task, or press F5 in VS Code.'
