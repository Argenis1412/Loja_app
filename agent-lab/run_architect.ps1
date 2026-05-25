# run_architect.ps1
# Execute Architect Agent to analyze Scout findings

param(
    [Parameter(Mandatory=$false)]
    [string]$ScoutInput = "scout_output_sample.json",
    [switch]$Help
)

if ($Help) {
    Write-Host "Usage: .\run_architect.ps1 [scout_json_file]"
    Write-Host ""
    Write-Host "Executes the Architect Agent (Claude 3.5 Sonnet)"
    Write-Host "Analyzes Scout findings and generates implementation plan"
    Write-Host ""
    Write-Host "Parameters:"
    Write-Host "  -ScoutInput       Path to Scout JSON output (default: scout_output_sample.json)"
    Write-Host ""
    Write-Host "Output: logs/architect_claude_output.json"
    Write-Host "Cost: ~$0.10-0.50 per run"
    exit 0
}

Write-Host "🏗️  Starting Architect Agent..." -ForegroundColor Cyan

# Check .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "   Copy .env.example to .env and add your API keys"
    exit 1
}

# Check ANTHROPIC_API_KEY
$env:ANTHROPIC_API_KEY = if (Test-Path ".env") {
    (Select-String -Path ".env" -Pattern "^ANTHROPIC_API_KEY=(.+)$" | ForEach-Object { $_.Matches.Groups[1].Value })
} else { $null }

if (-not $env:ANTHROPIC_API_KEY) {
    Write-Host "❌ ANTHROPIC_API_KEY not set in .env" -ForegroundColor Red
    exit 1
}

# Check Scout input exists
if (-not (Test-Path $ScoutInput)) {
    Write-Host "❌ Scout input file not found: $ScoutInput" -ForegroundColor Red
    Write-Host "   Run: .\run_scout.ps1"
    exit 1
}

Write-Host "✓ Environment configured" -ForegroundColor Green
Write-Host "✓ Scout input found: $ScoutInput" -ForegroundColor Green

# Run architect
try {
    Write-Host ""
    Write-Host "Running: uv run python agents/architect.py $ScoutInput"
    Write-Host "---" -ForegroundColor DarkGray
    
    uv run python agents/architect.py $ScoutInput
    
    Write-Host "---" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "✅ Architect completed!" -ForegroundColor Green
    Write-Host "   Output: logs/architect_claude_output.json"
}
catch {
    Write-Host "❌ Architect failed: $_" -ForegroundColor Red
    exit 1
}
