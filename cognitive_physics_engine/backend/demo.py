"""
Demonstration script for Cognitive Physics Engine

This script showcases the full capabilities of the system.
"""

import sys
import os

# Add cpe to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cpe'))

from cpe import WorldSimulator


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*70)
    print("🌍 COGNITIVE PHYSICS ENGINE - DEMONSTRATION")
    print("="*70)
    print("\nA prototype 'World Simulator' that computes truth in curved space")
    print("Combining Geomstats (Geometry) + PyTorch (Dynamics) + LLM (Semantics)")
    print("\n" + "="*70 + "\n")


def demo_1_basic_query():
    """Demo 1: Basic query"""
    print("\n" + "-"*70)
    print("📌 DEMO 1: Basic Query")
    print("-"*70 + "\n")
    
    simulator = WorldSimulator(
        backend='numpy',
        hidden_dim=64,
        n_layers=2,
        friction=0.1
    )
    
    result = simulator.query(
        question="What is the outlook for NVIDIA stock?",
        n_viewpoints=80,
        diversity=0.3,
        simulation_time=5.0,
        dt=0.1,
        method='euler'
    )
    
    print("\n📊 RESULTS:")
    print(f"  Question: {result['question']}")
    print(f"  Consensus: {result['consensus']}")
    print(f"  Confidence: {result['confidence']:.1%}")
    print(f"  Clusters: {result['n_clusters']}")
    

def demo_2_with_news():
    """Demo 2: Query with breaking news"""
    print("\n" + "-"*70)
    print("📌 DEMO 2: Query with Breaking News Injection")
    print("-"*70 + "\n")
    
    simulator = WorldSimulator(
        backend='numpy',
        hidden_dim=64,
        n_layers=2,
        friction=0.1
    )
    
    question = "Should I invest in NVIDIA?"
    
    # First query without news
    print("🔹 Baseline (without news):")
    result1 = simulator.query(
        question=question,
        n_viewpoints=80,
        simulation_time=5.0,
        dt=0.1
    )
    print(f"  Consensus: {result1['consensus']}")
    print(f"  Confidence: {result1['confidence']:.1%}\n")
    
    # Inject breaking news
    print("📰 Injecting breaking news...")
    simulator.inject_information(
        "BREAKING: NVIDIA announces record-breaking Q4 earnings, 70% revenue growth"
    )
    
    # Second query with news
    print("\n🔹 After bullish news:")
    result2 = simulator.query(
        question=question,
        n_viewpoints=80,
        simulation_time=5.0,
        dt=0.1
    )
    print(f"  Consensus: {result2['consensus']}")
    print(f"  Confidence: {result2['confidence']:.1%}")
    
    # Compare
    print("\n📈 IMPACT:")
    confidence_change = (result2['confidence'] - result1['confidence']) * 100
    print(f"  Confidence change: {confidence_change:+.1f} percentage points")


def demo_3_scenario_comparison():
    """Demo 3: Scenario comparison"""
    print("\n" + "-"*70)
    print("📌 DEMO 3: Multi-Scenario Comparison")
    print("-"*70 + "\n")
    
    simulator = WorldSimulator(
        backend='numpy',
        hidden_dim=64,
        n_layers=2,
        friction=0.1
    )
    
    question = "What is the long-term outlook for AI chip manufacturers?"
    
    scenarios = [
        "Scenario A: AI adoption accelerates, massive demand growth",
        "Scenario B: Economic recession reduces tech spending",
        "Scenario C: New competitor disrupts the GPU market"
    ]
    
    print(f"Base Question: {question}\n")
    
    results = simulator.compare_scenarios(
        question=question,
        scenarios=scenarios,
        n_viewpoints=60,
        simulation_time=4.0
    )
    
    print("\n📊 COMPARISON RESULTS:")
    
    for key, result in results.items():
        print(f"\n{key.upper().replace('_', ' ')}:")
        print(f"  Consensus: {result['consensus']}")
        print(f"  Confidence: {result['confidence']:.1%}")
        print(f"  Clusters: {result['n_clusters']}")


def demo_4_manifold_exploration():
    """Demo 4: Explore the manifold structure"""
    print("\n" + "-"*70)
    print("📌 DEMO 4: Manifold Structure Exploration")
    print("-"*70 + "\n")
    
    simulator = WorldSimulator(backend='numpy', hidden_dim=64, n_layers=2)
    
    # Different types of statements
    test_cases = [
        ("NVIDIA Q4 earnings: $22.1B revenue, up 265% YoY", "L1 Fact"),
        ("Analysis shows NVIDIA dominates 90% of GPU market", "L2 Data"),
        ("Strategic recommendation: Long position on semiconductor stocks", "L3 Strategy"),
        ("I believe AI chip demand will continue growing", "L4 Opinion"),
        ("Maybe quantum chips will replace GPUs in 5 years", "L5 Speculation"),
    ]
    
    print("🗺️  Mapping different statement types to the manifold:\n")
    
    for text, expected_level in test_cases:
        coord = simulator.translator.text_to_coordinate(text)
        interpretation = simulator.manifold.interpret_point(coord)
        
        print(f"Statement: {text[:60]}...")
        print(f"  Expected: {expected_level}")
        print(f"  Detected: {interpretation['level']}")
        print(f"  Coordinates: Z={coord[0]:.2f}, X={coord[2]:.2f}, W={coord[3]:.2f}")
        print()


def demo_5_convergence_analysis():
    """Demo 5: Analyze convergence patterns"""
    print("\n" + "-"*70)
    print("📌 DEMO 5: Convergence Pattern Analysis")
    print("-"*70 + "\n")
    
    simulator = WorldSimulator(backend='numpy', hidden_dim=64, n_layers=2)
    
    question = "Is artificial general intelligence achievable in 10 years?"
    
    print(f"Question: {question}\n")
    
    # Test different parameters
    configs = [
        (50, 5.0, "Few viewpoints, short time"),
        (100, 10.0, "Medium viewpoints, medium time"),
        (200, 15.0, "Many viewpoints, long time"),
    ]
    
    print("Testing different simulation parameters:\n")
    
    for n_viewpoints, sim_time, desc in configs:
        result = simulator.query(
            question=question,
            n_viewpoints=n_viewpoints,
            simulation_time=sim_time,
            dt=0.1
        )
        
        print(f"{desc}:")
        print(f"  N={n_viewpoints}, T={sim_time}s")
        print(f"  Confidence: {result['confidence']:.1%}")
        print(f"  Clusters: {result['n_clusters']}")
        print()


def main():
    """Run all demonstrations"""
    print_banner()
    
    demos = [
        ("Basic Query", demo_1_basic_query),
        ("Breaking News", demo_2_with_news),
        ("Scenario Comparison", demo_3_scenario_comparison),
        ("Manifold Exploration", demo_4_manifold_exploration),
        ("Convergence Analysis", demo_5_convergence_analysis),
    ]
    
    print("Available demonstrations:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print("  0. Run all\n")
    
    try:
        choice = input("Select demonstration (0-5): ").strip()
        
        if choice == '0':
            for name, demo_func in demos:
                try:
                    demo_func()
                except Exception as e:
                    print(f"\n⚠️  Error in {name}: {str(e)}\n")
        elif choice in ['1', '2', '3', '4', '5']:
            idx = int(choice) - 1
            demos[idx][1]()
        else:
            print("Invalid choice. Running demo 1...")
            demo_1_basic_query()
            
    except KeyboardInterrupt:
        print("\n\nDemonstration interrupted.")
    except Exception as e:
        print(f"\n⚠️  Error: {str(e)}")
        print("Running default demo...")
        demo_1_basic_query()
    
    print("\n" + "="*70)
    print("✅ DEMONSTRATION COMPLETE")
    print("="*70 + "\n")
    
    print("Next steps:")
    print("  1. Start the API server: python server.py")
    print("  2. Open the web interface: frontend/index.html")
    print("  3. Explore the code: cognitive_physics_engine/backend/cpe/")
    print()


if __name__ == "__main__":
    main()
