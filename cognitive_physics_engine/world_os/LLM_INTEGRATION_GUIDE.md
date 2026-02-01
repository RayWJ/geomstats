# 🤖 LLM Integration Guide for WorldOS v61.0

**Date**: 2026-02-01  
**Version**: v61.0  
**Status**: Real LLM integration available (with intelligent fallback)

---

## 📋 Overview

WorldOS v61.0 includes **real LLM integration** for cognitive decision-making. The system supports:

1. ✅ **OpenAI GPT-4** (primary)
2. ✅ **OpenAI GPT-3.5-Turbo** (cost-effective)
3. ✅ **Custom OpenAI-compatible APIs** (e.g., Azure, local models)
4. ✅ **Intelligent fallback** (rule-based when LLM unavailable)

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install openai
```

### Step 2: Set API Key

**Option A: Environment Variable** (Recommended)
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

**Option B: Pass to WorldOS**
```python
from engine import WorldOS

world = WorldOS(
    llm_model="gpt-4",
    llm_api_key="sk-your-api-key-here"
)
```

### Step 3: Run WorldOS

```bash
cd cognitive_physics_engine/world_os
python engine.py
```

Output will show:
```
  Initializing LLM agent...
✓ LLM Agent initialized (model: gpt-4)
```

---

## 🎯 LLM Capabilities

### 1. Trajectory Analysis

The LLM analyzes state transitions and provides insights:

**Input:**
- Initial state (level, domain, stance, intent)
- Final state
- Physics metrics (distance, drift, volatility)
- Entity context

**Output:**
```
Analysis: The entity moved from L2 (logic) to L1 (facts), indicating
a shift toward more concrete, data-driven positioning. The stance
flipped from bullish to bearish (distance: 2.34), suggesting a
significant sentiment reversal. Volatility of 0.45 indicates moderate
uncertainty during the transition.
```

### 2. Intervention Decisions

The LLM decides whether and how to intervene:

**Output:**
```json
{
  "should_intervene": true,
  "confidence": 0.85,
  "reasoning": "Rapid bearish shift with high cognitive distance indicates potential risk. Recommend defensive positioning.",
  "recommended_actions": [
    "Reduce exposure to volatile sectors",
    "Monitor for further sentiment deterioration",
    "Prepare contingency strategies"
  ]
}
```

### 3. Potential Field Extraction

The LLM converts natural language to potential fields:

**Input:**
```
Goal: Maintain bullish momentum in AI sector while managing
overvaluation risk. Avoid excessive shadow exposure.
```

**Output:**
```json
{
  "attractors": [
    {
      "description": "AI sector bullish momentum",
      "strength": 0.7,
      "target": {"level": "L3", "domain": "tech", "stance": 0.8, "intent": 0.6}
    }
  ],
  "barriers": [
    {
      "description": "Overvaluation risk zone",
      "strength": 0.8,
      "target": {"level": "L1", "domain": "tech", "stance": 0.9, "intent": -0.8}
    }
  ]
}
```

### 4. Narrative Generation

The LLM creates human-readable summaries:

**Output:**
```
NVIDIA experienced a significant trajectory shift, moving from strategic
positioning (L2) to tactical execution (L1) amid GPU supply concerns.
The sentiment reversal from bullish to bearish reflects market uncertainty
about near-term demand. Recommend close monitoring of sector dynamics.
```

---

## ⚙️ Configuration Options

### Basic Configuration

```python
from engine import WorldOS

world = WorldOS(
    world_state_dir="world_state",
    llm_model="gpt-4",              # Model to use
    llm_api_key=None,                # API key (or use env var)
    tick_duration=1.0,
    gamma=0.3,
    sigma=0.05
)
```

### Model Selection

| Model | Cost | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| **gpt-4** | $$$ | Slow | Excellent | Production, critical decisions |
| **gpt-3.5-turbo** | $ | Fast | Good | Development, high-frequency |
| **gpt-4-turbo** | $$ | Medium | Excellent | Balanced performance |

### Custom Base URL

For Azure OpenAI or local models:

```python
from brain.llm_agent import LLMAgent

agent = LLMAgent(
    model="gpt-4",
    api_key="your-key",
    base_url="https://your-azure-endpoint.openai.azure.com/"
)
```

---

## 🧪 Testing LLM Integration

### Test 1: LLM Agent Standalone

```bash
cd world_os/brain
python llm_agent.py
```

Expected output (with OpenAI):
```
✓ LLM Agent initialized (model: gpt-4)

TEST 1: Trajectory Analysis
Status: success
Model: gpt-4
Tokens used: 456

Analysis:
[GPT-4 generated analysis...]
```

### Test 2: WorldOS with LLM

```bash
cd world_os
python engine.py
```

Expected output:
```
🧠 [3/4] DECIDE: Cognitive processing...
  📊 Analysis (gpt-4): [Real LLM analysis]...
  ⚠️  Intervention: [LLM reasoning]
  📋 Recommended actions:
      - [Action 1]
      - [Action 2]
```

---

## 💡 Fallback Behavior

### When Fallback Activates

The system automatically falls back to rule-based logic when:
1. OpenAI library not installed
2. No API key provided
3. API call fails (network, quota, etc.)

### Fallback Quality

The fallback system provides basic functionality:

**Trajectory Analysis:**
- Detects level changes
- Identifies stance shifts
- Flags significant movement (distance > 1.0)

**Intervention Decisions:**
- Keyword-based heuristics
- Conservative recommendations
- 50% confidence baseline

**Potential Extraction:**
- Simple keyword matching ("bullish" → attractor)
- Basic risk detection ("avoid" → barrier)

### Fallback Output Example

```
  📊 Analysis (rule-based): Level shifted from L2 to L1. 
      Stance changed from bullish to bearish. 
      Significant movement detected (distance: 2.34).
  ⚠️  Intervention: Rule-based heuristic (no LLM available)
```

---

## 📊 Cost Estimation

### API Cost (OpenAI Pricing as of 2024)

| Model | Input | Output | Typical Tick Cost |
|-------|-------|--------|-------------------|
| GPT-4 | $0.03/1K | $0.06/1K | ~$0.03 |
| GPT-3.5-Turbo | $0.001/1K | $0.002/1K | ~$0.002 |
| GPT-4-Turbo | $0.01/1K | $0.03/1K | ~$0.015 |

### Budget Planning

For a typical simulation:
- **5-tick episode**: $0.01-$0.15
- **100-tick day**: $0.20-$3.00
- **Monthly (3000 ticks)**: $6-$90

**Optimization tips:**
1. Use GPT-3.5-Turbo for frequent ticks
2. Reserve GPT-4 for critical interventions
3. Adjust `llm_frequency` (e.g., every 5 ticks instead of 2)
4. Use fallback for non-critical entities

---

## 🔐 Security Best Practices

### 1. API Key Management

**DO:**
- ✅ Use environment variables
- ✅ Store in `.env` file (add to `.gitignore`)
- ✅ Use secrets management (AWS Secrets, Azure Key Vault)
- ✅ Rotate keys regularly

**DON'T:**
- ❌ Hardcode in source code
- ❌ Commit to version control
- ❌ Share in logs or error messages

### 2. Rate Limiting

```python
# Implement rate limiting
import time

class RateLimitedWorldOS(WorldOS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_llm_call = 0
        self.min_interval = 1.0  # 1 second between calls
    
    def tick(self, entity_id, **kwargs):
        # Ensure minimum interval between LLM calls
        if kwargs.get('llm_intervention'):
            elapsed = time.time() - self.last_llm_call
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_llm_call = time.time()
        
        return super().tick(entity_id, **kwargs)
```

### 3. Error Handling

The LLM agent includes robust error handling:
- Network failures → fallback
- API quota exceeded → fallback + warning
- Malformed responses → fallback + log

---

## 🔧 Troubleshooting

### Issue 1: "OpenAI library not available"

**Solution:**
```bash
pip install openai
```

### Issue 2: "API key not found"

**Solution:**
```bash
export OPENAI_API_KEY="sk-..."
# Or
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.bashrc
source ~/.bashrc
```

### Issue 3: "Rate limit exceeded"

**Solution:**
- Reduce `llm_frequency` in episode runner
- Switch to GPT-3.5-Turbo (higher quota)
- Implement exponential backoff

### Issue 4: "LLM calls too slow"

**Solution:**
- Use GPT-3.5-Turbo (10× faster)
- Reduce `max_tokens` in prompts
- Enable async mode (future feature)

### Issue 5: "Unexpected LLM responses"

**Solution:**
- Check `temperature` setting (lower = more deterministic)
- Use `response_format={"type": "json_object"}` for structured outputs
- Add explicit examples in system prompt

---

## 📈 Performance Tuning

### 1. Selective LLM Usage

```python
# Use LLM only for important events
def should_use_llm(distance, entity_value):
    if distance > 2.0:  # Significant movement
        return True
    if entity_value > 1000000:  # High-value entity
        return True
    return False

result = world.tick(
    entity_id="nvidia",
    llm_intervention=should_use_llm(distance, value)
)
```

### 2. Caching

```python
# Cache LLM responses for similar trajectories
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_analysis(trajectory_hash):
    return llm.analyze_trajectory(...)
```

### 3. Batch Processing

```python
# Analyze multiple entities in one LLM call
entities = ["nvidia", "tsmc", "intel"]
analyses = llm.analyze_batch(entities)
```

---

## 🚀 Advanced Usage

### Custom System Prompt

```python
from brain.llm_agent import LLMAgent

agent = LLMAgent(model="gpt-4")

# Override system prompt
custom_prompt = """You are a risk-focused analyst.
Always prioritize downside protection over upside capture.
Flag any shadow activity (W < -0.3) as high risk."""

agent._system_prompt = custom_prompt
```

### Multi-Model Ensemble

```python
# Use GPT-4 for analysis, GPT-3.5 for narrative
analyst = LLMAgent(model="gpt-4")
narrator = LLMAgent(model="gpt-3.5-turbo")

analysis = analyst.analyze_trajectory(...)
narrative = narrator.generate_narrative(analysis, entity_name)
```

---

## 📚 API Reference

### LLMAgent Class

```python
class LLMAgent:
    def __init__(self, api_key, model, base_url)
    
    def analyze_trajectory(initial_state, final_state, 
                          trajectory_stats, entity_context) -> Dict
    
    def decide_intervention(analysis, risk_threshold) -> Dict
    
    def extract_potential_field(natural_language) -> Dict
    
    def generate_narrative(trajectory_analysis, entity_name) -> str
```

### Return Types

**analyze_trajectory():**
```python
{
    "status": "success",
    "analysis": "...",
    "model": "gpt-4",
    "tokens_used": 456
}
```

**decide_intervention():**
```python
{
    "should_intervene": bool,
    "confidence": 0.0-1.0,
    "reasoning": "...",
    "recommended_actions": ["...", "..."]
}
```

---

## 🎯 Best Practices

1. **Start with fallback** to verify system works
2. **Enable LLM** for production runs
3. **Monitor costs** with token tracking
4. **Use GPT-3.5** for development
5. **Reserve GPT-4** for critical decisions
6. **Cache aggressively** for repeated patterns
7. **Log all LLM calls** for debugging
8. **Implement timeouts** for long-running calls

---

## 🌟 Conclusion

WorldOS v61.0 includes production-ready LLM integration with:
- ✅ Real GPT-4/3.5-Turbo support
- ✅ Intelligent fallback system
- ✅ Comprehensive error handling
- ✅ Cost-effective operation
- ✅ Easy configuration

**No more mocks!** 🎉

The LLM agent is fully functional and ready for real-world deployment.

---

**Next Steps:**
1. Install OpenAI library: `pip install openai`
2. Set API key: `export OPENAI_API_KEY="..."`
3. Run demo: `python engine.py`
4. Monitor costs and optimize

For support, see: `WORLDOS_V61_FINAL_REPORT.md`

---

*Last updated: 2026-02-01*
