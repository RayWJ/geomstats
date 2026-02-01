"""
WorldSimulator: The main cognitive physics engine

This is the "reactor" that combines all components:
1. Manifold (geometry)
2. Dynamics (physics)
3. Translator (semantics)

Pipeline:
User Query → Generate Viewpoints → Simulate Collapse → Synthesize Consensus
"""

import torch
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
import time

from .manifold import CognitiveManifold
from .dynamics import CognitiveDynamics
from .translator import Translator


class WorldSimulator:
    """
    The main cognitive physics engine.
    
    This orchestrates the full pipeline:
    1. Accept natural language query
    2. Generate diverse initial viewpoints
    3. Simulate physical collapse on manifold
    4. Extract Nash equilibria (truth attractors)
    5. Synthesize consensus in natural language
    """
    
    def __init__(
        self,
        backend: str = 'numpy',
        hidden_dim: int = 128,
        n_layers: int = 3,
        friction: float = 0.1,
        llm=None
    ):
        """
        Initialize the world simulator.
        
        Args:
            backend: 'numpy', 'autograd', or 'pytorch'
            hidden_dim: Hidden dimension for dynamics network
            n_layers: Number of layers in dynamics network
            friction: Friction coefficient
            llm: Optional LLM client
        """
        print("🌍 Initializing World Simulator...")
        
        # Component 1: Geometry
        print("  📐 Creating cognitive manifold (6D Riemannian space)...")
        self.manifold = CognitiveManifold(backend=backend)
        
        # Component 2: Physics
        print("  ⚛️  Initializing dynamics (Neural ODE engine)...")
        self.dynamics = CognitiveDynamics(
            manifold=self.manifold,
            hidden_dim=hidden_dim,
            n_layers=n_layers,
            friction=friction
        )
        
        # Component 3: Semantics
        print("  🧠 Connecting translator (LLM ↔ Geometry bridge)...")
        self.translator = Translator(
            manifold=self.manifold,
            dynamics=self.dynamics,
            llm=llm
        )
        
        print("✓ World Simulator ready!\n")
    
    def query(
        self,
        question: str,
        n_viewpoints: int = 100,
        diversity: float = 0.3,
        simulation_time: float = 10.0,
        dt: float = 0.1,
        method: str = 'euler',
        return_details: bool = False
    ) -> Dict[str, Any]:
        """
        Main query interface: Ask a question, get a consensus answer.
        
        Full pipeline:
        1. Parse question
        2. Generate N diverse viewpoints
        3. Map viewpoints to manifold coordinates
        4. Simulate collapse under potential field
        5. Analyze equilibrium clusters
        6. Synthesize natural language consensus
        
        Args:
            question: Natural language question
            n_viewpoints: Number of initial viewpoints to generate
            diversity: How diverse should initial viewpoints be
            simulation_time: How long to simulate (higher = more convergence)
            dt: Time step for integration
            method: Integration method ('euler' or 'rk4')
            return_details: Return full simulation trajectory
            
        Returns:
            Dictionary containing:
            - consensus: Natural language answer
            - confidence: Confidence score (0-1)
            - clusters: Number of equilibrium clusters
            - details: Optional detailed information
        """
        print(f"\n{'='*60}")
        print(f"📝 QUERY: {question}")
        print(f"{'='*60}\n")
        
        # Step 1: Generate initial viewpoints
        print(f"🌱 Generating {n_viewpoints} diverse viewpoints...")
        start_time = time.time()
        
        initial_points = self.translator.generate_viewpoints(
            query=question,
            n_viewpoints=n_viewpoints,
            diversity=diversity
        )
        
        print(f"   Initial spread: {initial_points.std(dim=0).mean():.4f}")
        print(f"   Time: {time.time() - start_time:.3f}s\n")
        
        # Step 2: Simulate collapse
        print(f"⚡ Simulating collapse (T={simulation_time}s, dt={dt})...")
        start_time = time.time()
        
        final_points, trajectory = self.dynamics.simulate_collapse(
            initial_points=initial_points,
            T=simulation_time,
            dt=dt,
            method=method,
            return_trajectory=return_details
        )
        
        print(f"   Final spread: {final_points.std(dim=0).mean():.4f}")
        print(f"   Convergence: {(initial_points.std() - final_points.std()) / initial_points.std() * 100:.1f}%")
        print(f"   Time: {time.time() - start_time:.3f}s\n")
        
        # Step 3: Analyze equilibria
        print(f"🎯 Analyzing equilibrium clusters...")
        start_time = time.time()
        
        analysis = self.dynamics.analyze_equilibrium(
            final_points,
            threshold=0.5
        )
        
        print(f"   Found {analysis['n_clusters']} cluster(s)")
        for i, cluster in enumerate(analysis['clusters']):
            print(f"   - Cluster {i+1}: {cluster['size']} viewpoints")
        print(f"   Time: {time.time() - start_time:.3f}s\n")
        
        # Step 4: Synthesize consensus
        print(f"💭 Synthesizing consensus...")
        start_time = time.time()
        
        consensus = self.translator.synthesize_consensus(
            final_points,
            method='centroid'
        )
        
        # Calculate confidence based on convergence
        convergence_ratio = final_points.std(dim=0).mean() / initial_points.std(dim=0).mean()
        confidence = 1.0 - convergence_ratio.item()
        confidence = np.clip(confidence, 0.0, 1.0)
        
        print(f"   Confidence: {confidence:.2%}")
        print(f"   Time: {time.time() - start_time:.3f}s\n")
        
        print(f"{'='*60}")
        print(f"✨ CONSENSUS: {consensus}")
        print(f"{'='*60}\n")
        
        # Build result
        result = {
            'question': question,
            'consensus': consensus,
            'confidence': confidence,
            'n_clusters': analysis['n_clusters'],
            'n_viewpoints': n_viewpoints,
            'simulation_time': simulation_time
        }
        
        if return_details:
            result['details'] = {
                'initial_points': initial_points.cpu().numpy(),
                'final_points': final_points.cpu().numpy(),
                'trajectory': [t.cpu().numpy() for t in trajectory] if trajectory else None,
                'clusters': analysis['clusters'],
                'convergence_ratio': convergence_ratio.item()
            }
        
        return result
    
    def inject_information(self, information: str):
        """
        Inject new information to modify the potential field.
        
        This simulates "breaking news" that changes the landscape.
        
        Args:
            information: New information text
        """
        print(f"\n📰 Injecting new information...")
        print(f"   Info: {information}\n")
        
        self.translator.update_potential_field(information)
    
    def compare_scenarios(
        self,
        question: str,
        scenarios: List[str],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Compare multiple scenarios for the same question.
        
        Args:
            question: Base question
            scenarios: List of scenario descriptions
            **kwargs: Additional arguments for query()
            
        Returns:
            Dictionary comparing results across scenarios
        """
        print(f"\n🔬 Comparing {len(scenarios)} scenarios...\n")
        
        results = {}
        
        # Run base query
        print("--- Scenario 0: Baseline ---")
        baseline = self.query(question, **kwargs)
        results['baseline'] = baseline
        
        # Run each scenario
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n--- Scenario {i}: {scenario[:50]}... ---")
            
            # Inject scenario information
            self.inject_information(scenario)
            
            # Re-run query
            result = self.query(question, **kwargs)
            results[f'scenario_{i}'] = result
        
        return results
    
    def visualize_manifold_slice(
        self,
        points: np.ndarray,
        dim_x: int = 0,
        dim_y: int = 2,
        title: str = "Manifold Slice"
    ):
        """
        Create a 2D visualization of a manifold slice.
        
        Args:
            points: (N, 6) array of points
            dim_x: X-axis dimension (0-5)
            dim_y: Y-axis dimension (0-5)
            title: Plot title
        """
        try:
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(10, 8))
            plt.scatter(points[:, dim_x], points[:, dim_y], alpha=0.5, s=20)
            plt.xlabel(self.manifold.dim_names[dim_x])
            plt.ylabel(self.manifold.dim_names[dim_y])
            plt.title(title)
            plt.grid(True, alpha=0.3)
            plt.savefig(f'/home/user/webapp/cognitive_physics_engine/{title.replace(" ", "_")}.png', dpi=150)
            print(f"✓ Saved visualization: {title}.png")
        except ImportError:
            print("⚠️  Matplotlib not available for visualization")


def demo():
    """
    Run a demonstration of the World Simulator.
    """
    print("\n" + "="*60)
    print("🚀 COGNITIVE PHYSICS ENGINE DEMO")
    print("="*60 + "\n")
    
    # Initialize simulator
    simulator = WorldSimulator(
        backend='numpy',
        hidden_dim=64,
        n_layers=2,
        friction=0.1
    )
    
    # Example 1: Simple query
    print("\n📌 Example 1: Simple Query")
    result1 = simulator.query(
        question="What is the outlook for NVIDIA stock?",
        n_viewpoints=100,
        diversity=0.3,
        simulation_time=5.0,
        dt=0.1
    )
    
    # Example 2: With breaking news
    print("\n📌 Example 2: Query with Breaking News")
    
    simulator.inject_information(
        "BREAKING: NVIDIA announces major partnership with OpenAI"
    )
    
    result2 = simulator.query(
        question="What is the outlook for NVIDIA stock?",
        n_viewpoints=100,
        diversity=0.3,
        simulation_time=5.0,
        dt=0.1
    )
    
    # Example 3: Scenario comparison
    print("\n📌 Example 3: Scenario Comparison")
    
    scenarios = [
        "NVIDIA reports 50% revenue growth",
        "NVIDIA faces chip shortage crisis",
        "New competitor emerges in GPU market"
    ]
    
    comparison = simulator.compare_scenarios(
        question="Should I invest in NVIDIA?",
        scenarios=scenarios,
        n_viewpoints=80,
        simulation_time=3.0
    )
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETED")
    print("="*60 + "\n")


if __name__ == "__main__":
    demo()
