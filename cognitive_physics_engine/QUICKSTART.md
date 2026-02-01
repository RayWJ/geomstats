# Quick Start Guide - Cognitive Physics Engine

## 🚀 Quick Start

### Option 1: Run Demo (No Server Required)

```bash
cd cognitive_physics_engine/backend
pip install numpy torch geomstats
python demo.py
```

Select from 5 demonstration scenarios to see the system in action.

### Option 2: Start API Server

```bash
cd cognitive_physics_engine/backend

# Install dependencies
pip install -r requirements.txt

# Start server
python server.py
```

Server will be available at: **http://localhost:8000**

API documentation: **http://localhost:8000/docs**

### Option 3: Use Web Interface

1. Start the API server (Option 2)
2. Open `cognitive_physics_engine/frontend/index.html` in your browser
3. Enter a question and adjust parameters
4. Click "Run Simulation"

### Option 4: Use as Python Library

```python
from cpe import WorldSimulator

# Initialize
simulator = WorldSimulator(
    backend='numpy',
    hidden_dim=128,
    n_layers=3
)

# Ask a question
result = simulator.query(
    question="What is the outlook for NVIDIA stock?",
    n_viewpoints=100,
    simulation_time=10.0
)

print(f"Consensus: {result['consensus']}")
print(f"Confidence: {result['confidence']:.1%}")
```

## 📊 Example Queries

- "What is the outlook for NVIDIA stock?"
- "Should we invest in AI infrastructure?"
- "Is quantum computing ready for production?"
- "What are the risks of climate change?"

## 🔧 System Requirements

- Python 3.8+
- 2GB RAM minimum (more for larger simulations)
- No GPU required (CPU only)

## 📝 Key Parameters

- **n_viewpoints**: Number of initial viewpoints (10-1000)
- **diversity**: How diverse viewpoints are (0.1-1.0)
- **simulation_time**: How long to simulate (1-60 seconds)
- **dt**: Integration time step (0.01-1.0)

## 🌍 6D Manifold Dimensions

1. **Z (Level)**: L1 (Facts) → L5 (Speculation)
2. **Y (Domain)**: Tech, Finance, Politics, etc.
3. **X (Stance)**: Bearish ↔ Bullish
4. **W (Intent)**: Shadow ↔ Light  
5. **T (Time)**: Past ↔ Future
6. **S (Scale)**: Micro ↔ Macro

## 🎯 Understanding Results

- **Consensus**: Natural language synthesis of converged viewpoints
- **Confidence**: Based on convergence rate (0-100%)
- **Clusters**: Number of equilibrium points found
- Lower clusters + higher confidence = stronger consensus

## 💡 Tips

1. **More viewpoints** = more comprehensive but slower
2. **Longer simulation time** = better convergence
3. **Higher diversity** = explores wider opinion space
4. **Inject news** to see how new information changes consensus

## 🐛 Troubleshooting

**Import errors**: Make sure dependencies are installed
```bash
pip install numpy torch geomstats fastapi uvicorn pydantic
```

**Server won't start**: Check if port 8000 is available
```bash
lsof -i :8000  # Check what's using port 8000
```

**Low convergence**: Try:
- Increase simulation_time
- Decrease dt (smaller steps)
- Reduce diversity

## 📚 Learn More

- Read the full README: `cognitive_physics_engine/README.md`
- Explore the code: `cognitive_physics_engine/backend/cpe/`
- Run tests: `cognitive_physics_engine/backend/tests/test_cpe.py`

---

**"In curved space, the shortest path is truth."**
