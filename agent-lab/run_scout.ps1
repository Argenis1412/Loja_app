# run_scout.ps1
# Execute Scout Agent to analyze codebase structure

param(
    [switch]$Help
)

if ($Help) {
    Write-Host "Usage: .\run_scout.ps1"
    Write-Host ""
    Write-Host "Executes the Scout Agent (Gemini 2.5 Flash)"
    Write-Host "Analyzes codebase structure and generates findings"
    Write-Host ""
    Write-Host "Output: scout_output_sample.json"
    Write-Host "Cost: ~$0.01-0.05 per run"
    exit 0
}

Write-Host "🔍 Starting Scout Agent..." -ForegroundColor Cyan

# Check .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "   Copy .env.example to .env and add your API keys"
    exit 1
}

# Check GOOGLE_API_KEY
$env:GOOGLE_API_KEY = if (Test-Path ".env") {
    (Select-String -Path ".env" -Pattern "^GOOGLE_API_KEY=(.+)$" | ForEach-Object { $_.Matches.Groups[1].Value })
} else { $null }

if (-not $env:GOOGLE_API_KEY) {
    Write-Host "❌ GOOGLE_API_KEY not set in .env" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Environment configured" -ForegroundColor Green

# Run scout
try {
    Write-Host ""
    Write-Host "Running: uv run python agents/scout.py"
    Write-Host "---" -ForegroundColor DarkGray
    
    uv run python agents/scout.py
    
    Write-Host "---" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "✅ Scout completed!" -ForegroundColor Green
    Write-Host "   Output: scout_output_sample.json"
}
catch {
    Write-Host "❌ Scout failed: $_" -ForegroundColor Red
    exit 1
}
