$root = $PSScriptRoot

Start-Process powershell -ArgumentList @(
    '-NoExit',
    '-Command',
    "Set-Location -Path '$root\\backend'; . .\\.venv\\Scripts\\Activate.ps1; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
)

Start-Process powershell -ArgumentList @(
    '-NoExit',
    '-Command',
    "Set-Location -Path '$root\\frontend'; npm run dev"
)