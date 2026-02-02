"""
Raywu Nash Equilibrium Collapse via Frechet Mean

This implements the "cognitive collapse" as a proper Frechet Mean
on the Riemannian manifold, not just Euclidean averaging.

Nash Equilibrium in Raywu space = Point that minimizes sum of squared
geodesic distances to all agents.
"""

import numpy as np
from typing import List, Optional
import warnings
warnings.filterwarnings('ignore')


class FrechetMeanCollapse:
    """
    Compute Nash Equilibrium via Frechet Mean on Raywu Manifold.
    
    In Euclidean space: mean = argmin Σ ||x_i - μ||²
    In Riemannian space: mean = argmin Σ d²(x_i, μ)
    
    where d(·,·) is the geodesic distance on the manifold.
    """
    
    def __init__(self, manifold, max_iter=100, epsilon=1e-6):
        """
        Args:
            manifold: RaywuCognitiveManifold instance
            max_iter: Maximum gradient descent iterations
            epsilon: Convergence threshold
        """
        self.manifold = manifold
        self.max_iter = max_iter
        self.epsilon = epsilon
    
    def fit(self, points, weights=None):
        """
        Compute Frechet mean of points on the manifold.
        
        Algorithm:
        1. Initialize at Euclidean mean (warm start)
        2. Iteratively move towards gradient of energy function
        3. Use exponential map to stay on manifold
        
        Args:
            points: (N, dim) array of agent positions
            weights: (N,) array of agent weights (importance)
        
        Returns:
            mean_point: Frechet mean (Nash equilibrium)
        """
        points = np.array(points)
        N = len(points)
        
        if weights is None:
            weights = np.ones(N) / N
        else:
            weights = np.array(weights)
            weights = weights / weights.sum()  # Normalize
        
        # Initialize at weighted Euclidean mean
        current_mean = np.average(points, axis=0, weights=weights)
        
        print(f"\n🎯 Computing Nash Equilibrium via Frechet Mean...")
        print(f"   Agents: {N}, Weights: {weights[:5]}..." if N > 5 else f"   Agents: {N}, Weights: {weights}")
        
        # Gradient descent in tangent space
        for iteration in range(self.max_iter):
            # Compute weighted sum of log maps
            # This is the gradient direction in tangent space
            tangent_sum = np.zeros(self.manifold.total_dim)
            
            for i, point in enumerate(points):
                # Log map: tangent vector from current_mean to point_i
                log_vec = self.manifold.metric.log(point, current_mean)
                tangent_sum += weights[i] * log_vec
            
            # Check convergence
            gradient_norm = np.linalg.norm(tangent_sum)
            
            if iteration % 10 == 0:
                print(f"   Iteration {iteration}: gradient_norm = {gradient_norm:.6f}")
            
            if gradient_norm < self.epsilon:
                print(f"   ✓ Converged at iteration {iteration}")
                break
            
            # Step size (adaptive)
            step_size = 0.5 / (1 + iteration * 0.01)
            
            # Move along gradient
            # Exp map: move from current_mean along tangent_sum
            update_vec = step_size * tangent_sum
            current_mean = self.manifold.metric.exp(update_vec, current_mean)
        
        self.mean_ = current_mean
        self.n_iter_ = iteration + 1
        
        return current_mean
    
    def compute_dispersion(self, points, mean_point=None):
        """
        Compute dispersion around the mean.
        
        Dispersion = Σ d²(x_i, μ) / N
        
        Low dispersion = strong consensus
        High dispersion = scattered opinions
        """
        if mean_point is None:
            mean_point = self.mean_
        
        points = np.array(points)
        total_distance = 0.0
        
        for point in points:
            dist = self.manifold.cognitive_distance(mean_point, point)
            total_distance += dist ** 2
        
        dispersion = total_distance / len(points)
        return dispersion


class CognitiveCollapseSimulator:
    """
    Full simulation of cognitive collapse dynamics.
    
    Process:
    1. Initialize multiple agents with different viewpoints
    2. Apply Raywu physics (friction, shadow penalties)
    3. Compute Nash equilibrium via Frechet mean
    4. Analyze convergence and consensus strength
    """
    
    def __init__(self, manifold):
        self.manifold = manifold
        self.frechet_solver = FrechetMeanCollapse(manifold)
    
    def simulate_debate(
        self, 
        agent_states: List[dict],
        agent_weights: Optional[List[float]] = None
    ):
        """
        Simulate multi-agent debate converging to Nash equilibrium.
        
        Args:
            agent_states: List of dicts with keys:
                {level, domain, stance, intent, time, scale}
            agent_weights: Optional importance weights
        
        Returns:
            result: Dict with equilibrium point and analysis
        """
        print("\n" + "="*70)
        print("🌍 RAYWU COGNITIVE COLLAPSE SIMULATION")
        print("="*70)
        
        # Encode agents to manifold points
        print(f"\n📍 Encoding {len(agent_states)} agents to manifold...")
        agent_points = []
        
        for i, state in enumerate(agent_states):
            point = self.manifold.encode_agent_state(
                state['level'],
                state['domain'],
                state['stance'],
                state['intent'],
                state.get('time', 0.0),
                state.get('scale', 0.0)
            )
            agent_points.append(point)
            
            decoded = self.manifold.decode_agent_state(point)
            print(f"  Agent {i+1}: {decoded['level']} {decoded['domain']} "
                  f"{decoded['stance']} {decoded['intent']}")
        
        agent_points = np.array(agent_points)
        
        # Compute initial dispersion
        euclidean_mean = agent_points.mean(axis=0)
        initial_dispersion = self.frechet_solver.compute_dispersion(
            agent_points, euclidean_mean
        )
        print(f"\n📊 Initial dispersion (Euclidean mean): {initial_dispersion:.4f}")
        
        # Run Frechet mean collapse
        nash_point = self.frechet_solver.fit(agent_points, agent_weights)
        
        # Compute final dispersion
        final_dispersion = self.frechet_solver.compute_dispersion(
            agent_points, nash_point
        )
        
        # Convergence ratio
        convergence_ratio = 1.0 - (final_dispersion / initial_dispersion)
        
        print(f"\n📊 Final dispersion (Frechet mean): {final_dispersion:.4f}")
        print(f"   Convergence improvement: {convergence_ratio:.1%}")
        
        # Decode equilibrium
        nash_decoded = self.manifold.decode_agent_state(nash_point)
        
        print(f"\n🎯 Nash Equilibrium (Truth Point):")
        print(f"   Level: {nash_decoded['level']}")
        print(f"   Domain: {nash_decoded['domain']}")
        print(f"   Stance: {nash_decoded['stance']}")
        print(f"   Intent: {nash_decoded['intent']}")
        print(f"   Time Focus: {nash_decoded['time_focus']}")
        print(f"   Scale: {nash_decoded['scale']}")
        
        # Consensus strength
        if convergence_ratio > 0.7:
            consensus_strength = "STRONG"
        elif convergence_ratio > 0.4:
            consensus_strength = "MODERATE"
        else:
            consensus_strength = "WEAK"
        
        print(f"\n💪 Consensus Strength: {consensus_strength}")
        print("="*70 + "\n")
        
        return {
            'nash_equilibrium': nash_point,
            'nash_decoded': nash_decoded,
            'initial_dispersion': initial_dispersion,
            'final_dispersion': final_dispersion,
            'convergence_ratio': convergence_ratio,
            'consensus_strength': consensus_strength,
            'n_iterations': self.frechet_solver.n_iter_
        }
    
    def analyze_distances(self, agent_points):
        """
        Analyze pairwise cognitive distances between agents.
        """
        N = len(agent_points)
        distances = np.zeros((N, N))
        
        print("\n📏 Cognitive Distance Matrix:")
        for i in range(N):
            for j in range(i+1, N):
                dist = self.manifold.cognitive_distance(
                    agent_points[i], agent_points[j]
                )
                distances[i, j] = dist
                distances[j, i] = dist
                print(f"   Agent {i+1} ↔ Agent {j+1}: {dist:.4f}")
        
        return distances


# ============================================================================
# DEMO: Raywu Paradigm in Action
# ============================================================================

def demo_raywu_collapse():
    """
    Demonstrate Raywu cognitive collapse with real scenario.
    
    Scenario: "Should we invest in AI infrastructure?"
    
    Agents:
    1. L1 Auditor: Conservative, fact-based, bearish
    2. L3 Strategist: Balanced, bullish on long-term
    3. L5 Bull: Speculative, very bullish
    4. L5 Conspiracy: Speculative, shadow intent
    """
    from raywu_manifold import RaywuCognitiveManifold
    
    print("\n" + "🔥"*35)
    print("DEMO: RAYWU PARADIGM - COGNITIVE COLLAPSE")
    print("🔥"*35)
    
    # Initialize manifold
    manifold = RaywuCognitiveManifold()
    simulator = CognitiveCollapseSimulator(manifold)
    
    # Define agents
    agents = [
        {
            'name': 'L1 Auditor',
            'level': 1,
            'domain': 'finance',
            'stance': -0.3,  # Slightly bearish
            'intent': 0.9,   # Very transparent
            'time': 0.0,
            'scale': 0.0
        },
        {
            'name': 'L3 Strategist', 
            'level': 3,
            'domain': 'tech',
            'stance': 0.6,   # Bullish
            'intent': 0.7,   # Constructive
            'time': 0.5,     # Future-focused
            'scale': 0.4     # Macro view
        },
        {
            'name': 'L5 Speculator',
            'level': 5,
            'domain': 'tech',
            'stance': 0.9,   # Very bullish
            'intent': 0.3,   # Somewhat constructive
            'time': 0.8,     # Far future
            'scale': 0.7     # Very macro
        },
        {
            'name': 'L5 Conspiracy',
            'level': 5,
            'domain': 'politics',
            'stance': 0.5,
            'intent': -0.8,  # Shadow intent
            'time': -0.3,
            'scale': 0.0
        }
    ]
    
    # Weights (importance)
    weights = [0.4, 0.3, 0.2, 0.1]  # Auditor has most weight
    
    # Run simulation
    result = simulator.simulate_debate(agents, weights)
    
    # Interpret result
    print("\n🧠 INTERPRETATION:")
    
    if result['nash_decoded']['level'] in ['L1', 'L2']:
        certainty = "High certainty (fact-based)"
    elif result['nash_decoded']['level'] == 'L3':
        certainty = "Moderate certainty (strategic)"
    else:
        certainty = "Low certainty (speculative)"
    
    print(f"   Certainty: {certainty}")
    print(f"   Consensus: {result['consensus_strength']}")
    print(f"   Final stance: {result['nash_decoded']['stance']}")
    
    if result['nash_decoded']['intent'] == 'shadow':
        print(f"   ⚠️  WARNING: Shadow influence detected!")
        print(f"   → The conspiracy theorist's hidden agenda warped the metric")
        print(f"   → True equilibrium might be different without manipulation")
    
    return result


if __name__ == "__main__":
    demo_raywu_collapse()
