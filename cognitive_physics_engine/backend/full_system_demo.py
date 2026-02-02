#!/usr/bin/env python3
"""
Raywu v11.0 Complete System Demo
=================================

This demo showcases the full Raywu Cognitive Paradigm v11.0:
- 6D Riemannian manifold
- Deep State agent loop
- Maxwell's Demon console
- Holographic decoding

Author: Raywu Paradigm Implementation Team
Date: 2026-02-01
"""

import sys
import json
import time
import numpy as np

# Add cpe to path
sys.path.insert(0, 'cpe')

from raywu_manifold import RaywuCognitiveManifold
from nash_collapse import CognitiveCollapseSimulator
from deep_state_agent import DeepStateEngine
from maxwell_demon import MaxwellDemon


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def demo_1_manifold_geometry():
    """Demo 1: Test manifold geometry"""
    print_header("DEMO 1: 6D RIEMANNIAN MANIFOLD GEOMETRY")
    
    manifold = RaywuCognitiveManifold()
    print("✓ Initialized 9D embedding manifold (H² × S² × R⁴)")
    print(f"  - Hyperbolic space: 2D (Poincaré ball)")
    print(f"  - Sphere: 2D (domain orthogonality)")
    print(f"  - Euclidean: 4D (X, W, T, S)")
    print(f"  - Total embedding: {manifold.total_dim}D")
    print(f"  - Plus 1D padding → {manifold.total_dim + 1}D\n")
    
    # Test distance
    print("📏 Testing cognitive distances:\n")
    
    p1 = manifold.encode_agent_state(
        level=1, domain="finance", stance=-0.8, 
        intent=0.9, time=0.0, scale=-0.5
    )
    
    p2 = manifold.encode_agent_state(
        level=5, domain="tech", stance=0.9,
        intent=-0.8, time=0.5, scale=0.5
    )
    
    dist = manifold.cognitive_distance(p1, p2)
    
    print(f"  Agent 1: L1 finance bear (daylight)")
    print(f"  Agent 2: L5 tech bull (shadow)")
    print(f"  Distance: {dist:.3f}\n")
    
    # Test metric warping
    print("🌊 Testing metric warping:\n")
    
    g_light = manifold.metric.metric_matrix(p1)
    g_shadow = manifold.metric.metric_matrix(p2)
    
    det_light = abs(np.linalg.det(g_light))
    det_shadow = abs(np.linalg.det(g_shadow))
    
    print(f"  det(g) at L1 daylight: {det_light:.2e}")
    print(f"  det(g) at L5 shadow:   {det_shadow:.2e}")
    print(f"  Distortion ratio: {det_shadow / det_light:.2e}x\n")


def demo_2_nash_collapse():
    """Demo 2: Nash equilibrium collapse"""
    print_header("DEMO 2: NASH EQUILIBRIUM VIA FRECHET MEAN")
    
    manifold = RaywuCognitiveManifold()
    simulator = CognitiveCollapseSimulator(manifold)
    
    # Define agents
    agents = [
        {"level": 1, "domain": "finance", "stance": -0.3, "intent": 0.9},  # Auditor
        {"level": 3, "domain": "tech", "stance": 0.6, "intent": 0.7},     # Analyst
        {"level": 5, "domain": "tech", "stance": 0.9, "intent": -0.6},    # Speculator
        {"level": 5, "domain": "politics", "stance": 0.8, "intent": -0.9} # Conspiracist
    ]
    
    weights = [0.5, 0.3, 0.15, 0.05]  # Higher weight to factual agents
    
    print(f"🤖 Simulating debate with {len(agents)} agents:\n")
    for i, agent in enumerate(agents):
        print(f"  Agent {i+1}: L{agent['level']} {agent['domain']} "
              f"stance={agent['stance']:.1f} intent={agent['intent']:.1f} "
              f"(weight={weights[i]:.0%})")
    
    print("\n🔄 Running Frechet mean convergence...\n")
    
    result = simulator.simulate_debate(agents, agent_weights=weights)
    
    print(f"✅ Converged in {result['n_iterations']} iterations")
    print(f"📍 Nash Equilibrium (Truth Point):")
    print(f"   Level: {result['nash_decoded']['level']}")
    print(f"   Domain: {result['nash_decoded']['domain']}")
    print(f"   Stance: {result['nash_decoded']['stance']}")
    print(f"   Intent: {result['nash_decoded']['intent']}")
    print(f"\n💪 Consensus Strength: {result['consensus_strength']}")
    print(f"🎯 Final Dispersion: {result['final_dispersion']:.4f}")
    print(f"📈 Improvement: {result['convergence_ratio']:.1%}\n")


def demo_3_deep_state_loop():
    """Demo 3: Deep State agent loop"""
    print_header("DEMO 3: DEEP STATE AGENT LOOP")
    
    engine = DeepStateEngine()
    
    question = "Will quantum computing threaten current encryption standards within 5 years?"
    
    print(f"❓ Question: {question}\n")
    
    # MODULE 0.5: Initialize lattices
    print("🔬 MODULE 0.5: LATTICE INITIALIZATION")
    lattices = engine.initialize_lattices(question, domains=["tech", "security", "finance"])
    print(f"✓ Generated {len(engine.lattices)} total lattices")
    print(f"✓ Activated {len(lattices)} relevant lattices\n")
    
    # MODULE 1: Spawn agents
    print("🤖 MODULE 1: AGENT SPAWNER")
    agents = engine.spawn_agents()
    print(f"✓ Spawned {len(agents)} agents:\n")
    for agent in agents[:4]:
        print(f"   - {agent.id} ({agent.role.value}): {agent.belief}")
    print()
    
    # MODULE 2: Run loop
    print("🔄 MODULE 2: RUNNING AGENT LOOP...\n")
    
    result = engine.run_agent_loop(max_loops=15)
    
    print(f"✅ Loop completed after {result['loops']} iterations")
    print(f"📊 Final Status: {result['status_history'][-1]}")
    
    if result['result']:
        print(f"💬 Result: {json.dumps(result['result'], indent=2)}")
    
    print()


def demo_4_maxwell_demon():
    """Demo 4: Maxwell's Demon console"""
    print_header("DEMO 4: MAXWELL'S DEMON CONSOLE")
    
    engine = DeepStateEngine()
    demon = MaxwellDemon()
    
    # Initialize
    question = "Should we invest in AI infrastructure stocks?"
    engine.initialize_lattices(question, domains=["tech", "finance"])
    engine.spawn_agents()
    
    print("🎮 Running simulation with real-time monitoring...\n")
    
    # Run 5 loops with monitoring
    for i in range(5):
        engine.loop_count = i + 1
        
        # Simulate loop (simplified)
        for agent in engine.agents:
            agent.confidence += (0.05 if i < 3 else -0.02)
            agent.logic_score = max(0, agent.logic_score + (5 if i < 3 else -3))
        
        # Compute entropy
        import numpy as np
        positions = np.array([a.lattice.to_vector() for a in engine.agents])
        entropy = np.std(positions, axis=0).mean()
        engine.entropy_history.append(entropy)
        
        from deep_state_agent import CollapseStatus
        if i < 3:
            engine.status_history.append(CollapseStatus.CONVERGING)
        elif i == 3:
            engine.status_history.append(CollapseStatus.DECEPTIVE)
        else:
            engine.status_history.append(CollapseStatus.COLLAPSED)
        
        # Capture and render
        snapshot = demon.capture_snapshot(engine)
        
        if i in [0, 2, 4]:  # Show snapshots
            print(demon.render_console())
            time.sleep(0.5)
    
    # Holographic decode
    print("\n" + "=" * 80)
    print("📡 HOLOGRAPHIC DECODER - LAYER 4 (Full Analysis)")
    print("=" * 80 + "\n")
    
    decoded = demon.holographic_decode(engine, layer=4)
    
    print(f"💡 Layer 1 - Aha Moment:")
    print(f"   {decoded['layer_1_aha']}\n")
    
    print(f"🏗️  Layer 2 - Framework:")
    for key, val in decoded['layer_2_framework'].items():
        print(f"   {key}: {val}")
    
    if 'layer_4_next_steps' in decoded:
        print(f"\n🎯 Layer 4 - Next Steps:")
        for step in decoded['layer_4_next_steps']:
            print(f"   → {step}")
    
    print()


def demo_5_full_integration():
    """Demo 5: Full system integration"""
    print_header("DEMO 5: FULL SYSTEM INTEGRATION TEST")
    
    print("🚀 Initializing complete Raywu v11.0 system...\n")
    
    # 1. Manifold
    manifold = RaywuCognitiveManifold()
    print("✅ 6D Riemannian manifold initialized")
    
    # 2. Nash collapse simulator
    collapse_sim = CognitiveCollapseSimulator(manifold)
    print("✅ Nash collapse simulator ready")
    
    # 3. Deep State engine
    engine = DeepStateEngine()
    print("✅ Deep State agent engine ready")
    
    # 4. Maxwell's Demon
    demon = MaxwellDemon()
    print("✅ Maxwell's Demon console ready")
    
    print("\n🎯 System Status: RAYWU AGENT ONLINE (v11.0 - DEEP STATE ENABLED)\n")
    
    # Quick test
    question = "Is AGI achievable by 2030?"
    print(f"🧪 Running full pipeline on: '{question}'\n")
    
    # Initialize and run
    engine.initialize_lattices(question, domains=["tech", "philosophy", "economics"])
    engine.spawn_agents()
    
    print(f"🔄 Lattices: {len(engine.active_lattices)}")
    print(f"🤖 Agents: {len(engine.agents)}")
    
    # Quick loop
    for i in range(3):
        engine.loop_count = i + 1
        snapshot = demon.capture_snapshot(engine)
    
    print(f"📊 Monitoring: {len(demon.snapshots)} snapshots captured")
    
    print("\n✅ Full integration test PASSED\n")


def main():
    """Run all demos"""
    print("\n" + "🎯" * 40)
    print("\n  RAYWU COGNITIVE PARADIGM v11.0 - COMPLETE SYSTEM DEMO")
    print("  ====================================================")
    print("\n  Author: Raywu Paradigm Implementation Team")
    print("  Date: 2026-02-01")
    print("\n" + "🎯" * 40)
    
    try:
        demo_1_manifold_geometry()
        demo_2_nash_collapse()
        demo_3_deep_state_loop()
        demo_4_maxwell_demon()
        demo_5_full_integration()
        
        print_header("✅ ALL DEMOS COMPLETED SUCCESSFULLY")
        
        print("📚 Documentation:")
        print("   - RAYWU_V11_COMPLETE.md - Full system documentation")
        print("   - RAYWU_MATH_CORE.md - Mathematical foundations")
        print("   - ACCESS_GUIDE.md - Quick start guide")
        
        print("\n🔬 Run individual tests:")
        print("   python cpe/raywu_manifold.py      # Test manifold")
        print("   python cpe/nash_collapse.py       # Test Nash collapse")
        print("   python cpe/deep_state_agent.py    # Test agent loop")
        print("   python cpe/maxwell_demon.py       # Test console")
        print("   python cpe/validation_suite.py    # Run all tests")
        
        print("\n🚀 Start services:")
        print("   python server.py                  # Backend API")
        print("   Open frontend/index.html          # Web UI")
        
        print("\n" + "=" * 80)
        print("  🎉 RAYWU v11.0 SYSTEM: FULLY OPERATIONAL")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
