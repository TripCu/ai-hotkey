[CmdletBinding()]
param(
    [ValidateSet("full", "backend", "listener")]
    [string]$Mode = "full"
)

$ErrorActionPreference = "Stop"

function Resolve-Python {
    $candidates = @(
        @("py", "-3.12"),
        @("py", "-3.11"),
        @("py", "-3.10"),
        @("py", "-3.9"),
        @("python")
    )

    foreach ($candidate in $candidates) {
        $exe = $candidate[0]
        $args = $candidate[1..($candidate.Count - 1)]
        if ($args -eq $null) { $args = @() }
        try {
            $command = $args + @("-c", "import sys; print('.'.join(map(str, sys.version_info[:3])))")
            $output = & $exe @command 2>$null
            if ($LASTEXITCODE -eq 0 -and $output) {
                $version = [Version]$output.Trim()
                if ($version.Major -eq 3 -and $version.Minor -ge 9 -and $version.Minor -le 12) {
                    return @{ Path = $exe; Args = $args; Version = $version }
                }
            }
        } catch {
            continue
        }
    }
    throw "Python 3.9–3.12 is required. Install from https://www.python.org/downloads/windows/ before running this script."
}

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot
Write-Host "Working directory: $projectRoot" -ForegroundColor Cyan

$pythonInfo = Resolve-Python
$pythonCmd = $pythonInfo.Path
$pythonArgs = $pythonInfo.Args
Write-Host "Using Python $($pythonInfo.Version) via '$pythonCmd $($pythonArgs -join ' ')'." -ForegroundColor Cyan

$venvPath = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"

if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    & $pythonCmd $pythonArgs -m venv $venvPath
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor DarkGray
}

Write-Host "Upgrading pip..." -ForegroundColor Cyan
& $venvPython -m pip install --upgrade pip

Write-Host "Installing project dependencies..." -ForegroundColor Cyan
& $venvPython -m pip install -r requirements.txt

switch ($Mode) {
    "full" {
        Write-Host "Launching backend + listener (full stack)..." -ForegroundColor Green
        & $venvPython run.py
    }
    "backend" {
        Write-Host "Launching backend only..." -ForegroundColor Green
        & $venvPython run_backend.py
    }
    "listener" {
        Write-Host "Launching listener only..." -ForegroundColor Green
        Write-Host "Ensure backend is reachable at HOST:PORT before continuing." -ForegroundColor Yellow
        & $venvPython run_listener.py
    }
}
