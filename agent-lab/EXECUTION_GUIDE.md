# Agent Lab — Execution Guide

## 📋 Overview

The Agent Lab contains two specialized agents that work in sequence:

1. **Scout Agent** (`agents/scout.py`) — Analyzes codebase structure
   - Model: Gemini 2.5 Flash
   - Cost: Very low (~$0.01-0.05 per run)
   - Speed: Fast (< 10 seconds)

2. **Architect Agent** (`agents/architect.py`) — Analyzes Scout findings
   - Model: Claude 3.5 Sonnet
   - Cost: Higher (~$0.10-0.50 per run)
   - Speed: Moderate (10-30 seconds)

3. **Compare** (`compare_architects.py`) — Runs both models in parallel
   - Compares Gemini and Claude outputs
   - Generates structured comparison report

---

## 🔧 Setup

### Prerequisites
- Python 3.11+
- `uv` package manager (or `pip`)
- API keys for Google Gemini and Anthropic Claude

### Environment Configuration

1. **Copy the template:**
   ```bash
   cp agent-lab/.env.example agent-lab/.env
   ```

2. **Fill in your API keys:**
   ```bash
   # agent-lab/.env
   GOOGLE_API_KEY=your-google-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   ```

3. **Install dependencies:**
   ```bash
   cd agent-lab
   uv sync
   # or: pip install -r requirements.txt (if available)
   ```

---

## 🚀 Execution Methods

### Option 1: Run Comparison (Both Models)
Run Scout + both Architect implementations (Gemini & Claude):

```bash
cd agent-lab
uv run python compare_architects.py
```

**Output:**
- `logs/architect_gemini_output.json` — Gemini's structured analysis
- `logs/architect_claude_output.json` — Claude's structured analysis
- `logs/architect_comparison.json` — Side-by-side comparison

**Cost:** ~$0.15-0.60 per run

---

### Option 2: Run Scout Only
Analyze codebase without Architect:

```bash
cd agent-lab
uv run python agents/scout.py
```

**Output:** Structured JSON with file inventory and findings

**Cost:** ~$0.01-0.05 per run

---

### Option 3: Run Architect Only
Analyze existing Scout output:

```bash
cd agent-lab
uv run python agents/architect.py <scout_json_file>
```

**Output:** `logs/architect_claude_output.json`

**Cost:** ~$0.10-0.50 per run

---

## 📊 Output Structure

### Scout Output
```json
{
  "timestamp": "ISO-8601",
  "scan_duration_s": 1.23,
  "files_analyzed": 42,
  "files_by_category": { ... },
  "code_metrics": { ... },
  "architectural_findings": [ ... ]
}
```

### Architect Output
```json
{
  "validated_findings": ["string"],
  "false_positives": ["string"],
  "systemic_risks": ["string"],
  "implementation_plan": [
    {
      "task_id": "string",
      "title": "string",
      "priority": "high|medium|low",
      "effort": "high|medium|low",
      "risk_level": "high|medium|low"
    }
  ],
  "blockers": ["string"]
}
```

---

## 💰 Cost Optimization

### Gemini Flash (Scout)
- **Price:** $0.075/1M input, $0.30/1M output tokens
- **When to use:** Frequent/exploratory analysis
- **Typical cost per run:** < $0.10

### Claude Sonnet (Architect)
- **Price:** $3.00/1M input, $15.00/1M output tokens
- **When to use:** Critical analysis, final review
- **Typical cost per run:** $0.10-0.50

### Money-Saving Tips
1. Run Scout first to identify high-impact areas
2. Use Architect only on validated findings
3. Batch multiple analyses in one session
4. Cache Scout output to avoid re-scanning

---

## 🔍 Troubleshooting

### Error: "GOOGLE_API_KEY not found"
- Verify `.env` exists in `agent-lab/` directory
- Check API key is valid: `echo $GOOGLE_API_KEY`

### Error: "ANTHROPIC_API_KEY not found"
- Same as above for Anthropic API

### Scout fails with timeout
- Reduce scope in `IGNORE_DIRS` in `agents/scout.py`
- Increase target size limit in configuration

### Architect produces invalid JSON
- Check Scout output format is valid
- Check API key quota/limits
- Review `logs/architect_*_output.json` for raw response

---

## 📝 Logging

All calls are logged to `logs/` directory:
- `architect_gemini_output.json` — Raw Gemini response
- `architect_claude_output.json` — Raw Claude response
- Call history in `logger.py`

Check these for debugging and cost tracking.

---

## 🎯 Next Steps

1. **Configuration:** Copy `.env.example` → `.env`, add keys
2. **First Run:** Execute `uv run python compare_architects.py`
3. **Review:** Check `logs/architect_comparison.json` for insights
4. **Iterate:** Use findings to refine codebase analysis strategy

