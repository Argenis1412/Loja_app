# Quick Start Guide

## ⚡ 5 Minutes to First Run

### Step 1: Setup Environment
```bash
cd agent-lab

# Copy template
cp .env.example .env

# Edit .env and add your API keys:
# - GOOGLE_API_KEY (for Gemini Scout)
# - ANTHROPIC_API_KEY (for Claude Architect)
```

### Step 2: Install Dependencies
```bash
# Option A: Using uv (recommended)
uv sync

# Option B: Using pip
pip install anthropic google-genai pydantic python-dotenv
```

### Step 3: Run Comparison
```bash
# Windows (PowerShell)
.\run_comparison.ps1

# macOS/Linux
python compare_architects.py
```

### Step 4: View Results
```bash
# Check outputs
cat logs/architect_comparison.json
```

---

## 🎯 Common Commands

| Goal | Command |
|------|---------|
| Quick codebase scan | `.\run_scout.ps1` |
| Analyze findings | `.\run_architect.ps1` |
| Full comparison | `.\run_comparison.ps1` |
| Get help | `.\run_scout.ps1 -Help` |

---

## 💰 Estimated Costs

- **Scout only:** $0.01-0.05
- **Architect only:** $0.10-0.50
- **Full comparison:** $0.15-0.60

---

## 🆘 Troubleshooting

**Error: API key not found**
- Verify `.env` exists in `agent-lab/` folder
- Check file has correct format: `KEY=value`

**Error: `uv` not found**
- Install: `pip install uv`
- Or use `python` instead of `uv run python`

**Error: Module not found**
- Run: `uv sync` or `pip install -r requirements.txt`

---

## 📚 Full Documentation

See [EXECUTION_GUIDE.md](./EXECUTION_GUIDE.md) for detailed information.

