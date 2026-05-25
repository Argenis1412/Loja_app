# run_comparison.ps1
# Execute Comparison - runs Scout + both Architect implementations

param(
    [switch]$Help
)

if ($Help) {
    Write-Host "Usage: .\run_comparison.ps1"
    Write-Host ""
    Write-Host "Executes full pipeline:"
    Write-Host "  1. Scout Agent (Gemini 2.5 Flash)"
    Write-Host "  2. Architect Agent - Gemini version"
    Write-Host "  3. Architect Agent - Claude version"
    Write-Host "  4. Generate comparison report"
    Write-Host ""
    Write-Host "Output:"
    Write-Host "  - logs/architect_gemini_output.json"
    Write-Host "  - logs/architect_claude_output.json"
    Write-Host "  - logs/architect_comparison.json"
    Write-Host ""
    Write-Host "Cost: ~$0.15-0.60 per full run"
    exit 0
}

Write-Host "🚀 Starting Full Comparison Pipeline..." -ForegroundColor Cyan

# Check .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "   Copy .env.example to .env and add your API keys"
    exit 1
}

# Check both API keys
$googleKey = if (Test-Path ".env") {
    (Select-String -Path ".env" -Pattern "^GOOGLE_API_KEY=(.+)$" | ForEach-Object { $_.Matches.Groups[1].Value })
} else { $null }

$anthropicKey = if (Test-Path ".env") {
    (Select-String -Path ".env" -Pattern "^ANTHROPIC_API_KEY=(.+)$" | ForEach-Object { $_.Matches.Groups[1].Value })
} else { $null }

if (-not $googleKey) {
    Write-Host "❌ GOOGLE_API_KEY not set in .env" -ForegroundColor Red
    exit 1
}

if (-not $anthropicKey) {
    Write-Host "❌ ANTHROPIC_API_KEY not set in .env" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Environment configured" -ForegroundColor Green
Write-Host ""

# Run comparison
try {
    Write-Host "Running: uv run python compare_architects.py"
    Write-Host "---" -ForegroundColor DarkGray
    
    uv run python compare_architects.py
    
    Write-Host "---" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "✅ Comparison completed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Outputs generated:"
    Write-Host "   - logs/architect_gemini_output.json"
    Write-Host "   - logs/architect_claude_output.json"
    Write-Host "   - logs/architect_comparison.json"
}
catch {
    Write-Host "❌ Comparison failed: $_" -ForegroundColor Red
    exit 1
}
