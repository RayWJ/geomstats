"""
Physics Engine - Langevin Dynamics on Riemannian Manifold
===========================================================

This module implements the continuous evolution of cognitive states.

Core Equation (Langevin Dynamics):
    dx/dt = -∇_g V(x) - γv + σdW
    
where:
    - ∇_g V: Riemannian gradient of potential (driving force)
    - γv: Damping/friction term (resistance)
    - σdW: Stochastic noise (uncertainty)

Philosophy:
- Between "interventions", the world evolves according to physics
- This is the "daydreaming" phase: "What happens if we do nothing?"
- The manifold's curvature naturally constraints impossible trajectories

Author: Raywu WorldOS Team
Date: 2026-02-01
Version: v61.0
"""

import numpy as np
from scipy.integrate import odeint
from typing import Callable, Dict, Any, Optional, Tuple
import warnings

try:
    from .manifold import CognitiveManifold, CognitiveFrictionMap
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from manifold import CognitiveManifold, CognitiveFrictionMap


class PotentialField:
    """
    Potential Field V(x) - The "Landscape" of Cognitive Space
    
    This encodes:
    - Attractors: Goals, targets (gravity wells)
    - Repellers: Constraints, boundaries (potential barriers)
    - Channels: Preferred paths (valleys)
    
    Physics Analogy: Like a marble rolling on a warped surface.
    """
    
    def __init__(self):
        """Initialize empty potential field."""
        self.wells = []      # Attractors
        self.barriers = []   # Repellers
    
    def add_attractor(self, position: np.ndarray, strength: float, radius: float = 1.0):
        """
        Add a gravity well (attractor).
        
        V_well = -strength * exp(-||x-pos||²/(2*radius²))
        
        Args:
            position: Target location
            strength: How strong the attraction (positive)
            radius: Effective range
        """
        self.wells.append({
            'position': np.array(position),
            'strength': strength,
            'radius': radius
        })
    
    def add_barrier(self, position: np.ndarray, strength: float, radius: float = 0.5):
        """
        Add a potential barrier (repeller).
        
        V_barrier = +strength * exp(-||x-pos||²/(2*radius²))
        
        Args:
            position: Center of barrier
            strength: How strong the repulsion (positive)
            radius: Effective range
        """
        self.barriers.append({
            'position': np.array(position),
            'strength': strength,
            'radius': radius
        })
    
    def __call__(self, x: np.ndarray) -> float:
        """
        Evaluate potential V(x) at position x.
        
        Total potential = Σ wells + Σ barriers
        """
        V = 0.0
        
        # Attractors (negative potential = downhill)
        for well in self.wells:
            diff = x - well['position']
            dist_sq = np.sum(diff ** 2)
            V -= well['strength'] * np.exp(-dist_sq / (2 * well['radius']**2))
        
        # Barriers (positive potential = uphill)
        for barrier in self.barriers:
            diff = x - barrier['position']
            dist_sq = np.sum(diff ** 2)
            V += barrier['strength'] * np.exp(-dist_sq / (2 * barrier['radius']**2))
        
        return V
    
    def gradient(self, x: np.ndarray, epsilon: float = 1e-5) -> np.ndarray:
        """
        Compute gradient ∇V(x) via finite differences.
        
        ∇V_i = (V(x + ε*e_i) - V(x - ε*e_i)) / (2ε)
        """
        grad = np.zeros_like(x)
        
        for i in range(len(x)):
            x_plus = x.copy()
            x_minus = x.copy()
            x_plus[i] += epsilon
            x_minus[i] -= epsilon
            
            grad[i] = (self(x_plus) - self(x_minus)) / (2 * epsilon)
        
        return grad


class PhysicsEngine:
    """
    The Physics Engine - Makes the World Move
    
    Implements Langevin dynamics on the cognitive manifold:
        dx/dt = v
        dv/dt = -∇_g V(x) - γv + σξ(t)
    
    Key Features:
    1. Riemannian gradient flow (respects manifold curvature)
    2. Damping (resistance to change)
    3. Stochastic noise (uncertainty)
    4. Constraint enforcement (stay on manifold)
    """
    
    def __init__(
        self,
        manifold: CognitiveManifold,
        gamma: float = 0.5,
        sigma: float = 0.1
    ):
        """
        Initialize physics engine.
        
        Args:
            manifold: The cognitive manifold
            gamma: Damping coefficient (default 0.5)
            sigma: Noise strength (default 0.1)
        """
        self.manifold = manifold
        self.gamma = gamma  # Friction/damping
        self.sigma = sigma  # Noise/uncertainty
    
    def riemannian_gradient(
        self,
        x: np.ndarray,
        potential: PotentialField
    ) -> np.ndarray:
        """
        Compute Riemannian gradient: ∇_g V = g^{-1} ∇V
        
        In flat space: ∇V is just the partial derivatives
        In curved space: Must use inverse metric to "lift" to tangent space
        
        Self-Verification:
        - g^{-1} transforms covariant vectors to contravariant
        - This ensures gradient points in "true" steepest descent direction
        """
        # 1. Compute Euclidean gradient ∇V
        grad_V = potential.gradient(x)
        
        # 2. Get metric at current point
        g = self.manifold.metric.metric_matrix(x)
        
        # 3. Compute Riemannian gradient: g^{-1} ∇V
        try:
            g_inv = np.linalg.inv(g)
            riem_grad = np.dot(g_inv, grad_V)
        except np.linalg.LinAlgError:
            # Metric is singular, use pseudo-inverse
            warnings.warn("Metric singular, using pseudo-inverse")
            g_inv = np.linalg.pinv(g)
            riem_grad = np.dot(g_inv, grad_V)
        
        return riem_grad
    
    def vector_field(
        self,
        state: np.ndarray,
        t: float,
        potential: PotentialField
    ) -> np.ndarray:
        """
        Vector field for Langevin ODE.
        
        State = [position, velocity]
        Returns: d/dt [position, velocity]
        
        Equations:
            dx/dt = v
            dv/dt = -∇_g V(x) - γv + noise
        """
        dim = len(state) // 2
        x = state[:dim]
        v = state[dim:]
        
        # 1. Position derivative: dx/dt = v
        dx_dt = v
        
        # 2. Velocity derivative: dv/dt = force - damping
        # Compute Riemannian gradient (driving force)
        grad_V = self.riemannian_gradient(x, potential)
        
        # Driving force (move downhill)
        force = -grad_V
        
        # Damping (resistance to motion)
        damping = -self.gamma * v
        
        # Combined acceleration
        dv_dt = force + damping
        
        # Numerical stability: Clip acceleration to reasonable bounds
        max_accel = 10.0
        dv_dt = np.clip(dv_dt, -max_accel, max_accel)
        
        # Note: Stochastic term σdW is added separately
        
        return np.concatenate([dx_dt, dv_dt])
    
    def project_to_manifold(self, x: np.ndarray) -> np.ndarray:
        """
        Project point back to manifold constraints.
        
        Constraints:
        1. Hyperbolic coords (0:3): ||h|| < 1 (Poincaré ball)
        2. Sphere coords (3:6): normalize to unit sphere
        3. Euclidean coords (6:10): clip to [-1, 1] to prevent overflow
        """
        x_proj = x.copy()
        
        # 1. Project hyperbolic coords to ball
        h_coords = x_proj[:3]
        h_norm = np.linalg.norm(h_coords)
        if h_norm >= 0.95:
            # Rescale to stay inside ball
            x_proj[:3] = h_coords * (0.95 / h_norm)
        
        # 2. Project sphere coords to unit sphere
        s_coords = x_proj[3:6]
        s_norm = np.linalg.norm(s_coords)
        if s_norm > 1e-6:
            x_proj[3:6] = s_coords / s_norm
        
        # 3. Euclidean coords: clip to reasonable bounds
        x_proj[6:10] = np.clip(x_proj[6:10], -1.0, 1.0)
        
        return x_proj
    
    def evolve(
        self,
        initial_state: np.ndarray,
        potential: PotentialField,
        time_span: float,
        dt: float = 0.1,
        initial_velocity: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Evolve system forward in time.
        
        Args:
            initial_state: Starting position (dim-dimensional)
            potential: Potential field V(x)
            time_span: How long to simulate (in arbitrary time units)
            dt: Time step for integration
            initial_velocity: Starting velocity (default: zero)
        
        Returns:
            final_position, trajectory
        """
        dim = len(initial_state)
        
        # Initialize velocity if not provided
        if initial_velocity is None:
            initial_velocity = np.zeros(dim)
        
        # Combined state: [position, velocity]
        state0 = np.concatenate([initial_state, initial_velocity])
        
        # Time points
        t_start, t_end = time_span
        t_eval = np.arange(t_start, t_end, dt)
        
        # Integrate ODE
        try:
            trajectory = odeint(
                self.vector_field,
                state0,
                t_eval,
                args=(potential,)
            )
        except Exception as e:
            warnings.warn(f"ODE integration failed: {e}. Returning initial state.")
            return initial_state, np.array([initial_state])
        
        # Extract positions (first half of state)
        positions = trajectory[:, :dim]
        
        # Project back to manifold (enforce constraints)
        positions_proj = np.array([self.project_to_manifold(x) for x in positions])
        
        # Add stochastic noise (simple Euler-Maruyama approximation)
        if self.sigma > 0:
            noise = np.random.normal(0, self.sigma * np.sqrt(dt), positions_proj.shape)
            positions_proj += noise
            # Re-project after noise
            positions_proj = np.array([self.project_to_manifold(x) for x in positions_proj])
        
        # Return final state and full trajectory
        final_position = positions_proj[-1]
        
        return final_position, positions_proj
    
    def analyze_trajectory(self, trajectory: np.ndarray) -> Dict[str, Any]:
        """
        Analyze trajectory to extract semantic information.
        
        Returns:
            Dictionary with analysis results:
            - drift: Net displacement
            - volatility: Standard deviation of steps
            - trend: Upward/downward/oscillating
            - convergence: Did it stabilize?
        """
        if len(trajectory) < 2:
            return {'drift': 0, 'volatility': 0, 'trend': 'static', 'convergence': True}
        
        # Compute displacement at each step
        displacements = np.diff(trajectory, axis=0)
        
        # Net drift (total displacement)
        drift = np.linalg.norm(trajectory[-1] - trajectory[0])
        
        # Volatility (std of step sizes)
        step_sizes = np.linalg.norm(displacements, axis=1)
        volatility = np.std(step_sizes)
        
        # Trend (is it moving consistently in one direction?)
        cumsum = np.cumsum(np.linalg.norm(displacements, axis=1))
        if len(cumsum) > 1:
            trend_slope = (cumsum[-1] - cumsum[0]) / len(cumsum)
            if trend_slope > 0.1:
                trend = 'increasing'
            elif trend_slope < -0.1:
                trend = 'decreasing'
            else:
                trend = 'stable'
        else:
            trend = 'stable'
        
        # Convergence (did it settle down?)
        # Check if last 20% of trajectory has low variance
        tail_len = max(2, len(trajectory) // 5)
        tail = trajectory[-tail_len:]
        tail_variance = np.var(tail, axis=0)
        convergence = np.mean(tail_variance) < 0.01
        
        return {
            'drift': float(drift),
            'volatility': float(volatility),
            'trend': trend,
            'convergence': convergence,
            'final_position': trajectory[-1].tolist()
        }


# ============================================================================
# DEMO & VALIDATION
# ============================================================================

def demo_physics():
    """
    Demonstrate the physics engine with a simple scenario.
    """
    print("\n" + "="*70)
    print("🌊 PHYSICS ENGINE DEMO - Langevin Dynamics")
    print("="*70 + "\n")
    
    # 1. Create manifold with friction
    friction_map = CognitiveFrictionMap()
    friction_map.add_source(
        position=np.array([0.5, 0, 0, 1, 0, 0, 0.5, 0.8, 0, 0]),
        strength=0.6,
        radius=0.8
    )
    
    manifold = CognitiveManifold(friction_map=friction_map)
    print("✓ Manifold initialized with friction source")
    
    # 2. Create potential field (goals and constraints)
    potential = PotentialField()
    
    # Goal: Move toward "successful bullish outcome"
    target = np.array([0.3, 0, 0, 0.8, 0.6, 0, 0.7, 0.9, 0.5, 0.3])
    potential.add_attractor(target, strength=0.5, radius=1.5)  # Reduced strength
    print("✓ Added attractor (goal state)")
    
    # Constraint: Avoid "bankruptcy zone"
    danger = np.array([0.8, 0, 0, -0.8, -0.6, 0, -0.9, -0.9, -0.5, -0.8])
    potential.add_barrier(danger, strength=1.0, radius=1.0)  # Reduced strength
    print("✓ Added barrier (danger zone)")
    
    # 3. Create physics engine
    physics = PhysicsEngine(manifold, gamma=0.3, sigma=0.05)
    print("✓ Physics engine ready (γ=0.3, σ=0.05)\n")
    
    # 4. Set initial state
    initial = manifold.encode_state(
        level=3, domain='tech', stance=0.2, intent=0.5, time=0.0, scale=0.0
    )
    print("Initial State:")
    print(f"  Position: {initial}")
    decoded = manifold.decode_state(initial)
    print(f"  Decoded: {decoded['level']}, {decoded['domain']}, {decoded['stance']}\n")
    
    # 5. Run simulation
    print("🚀 Running simulation (30 time units)...")
    final, trajectory = physics.evolve(initial, potential, time_span=30, dt=0.5)
    
    print(f"✓ Simulation complete ({len(trajectory)} steps)\n")
    
    # 6. Analyze results
    print("📊 Trajectory Analysis:")
    analysis = physics.analyze_trajectory(trajectory)
    print(f"  Drift: {analysis['drift']:.4f}")
    print(f"  Volatility: {analysis['volatility']:.4f}")
    print(f"  Trend: {analysis['trend']}")
    print(f"  Convergence: {analysis['convergence']}\n")
    
    print("Final State:")
    print(f"  Position: {final}")
    final_decoded = manifold.decode_state(final)
    print(f"  Decoded: {final_decoded['level']}, {final_decoded['domain']}, {final_decoded['stance']}")
    
    # 7. Distance traveled
    dist = manifold.cognitive_distance(initial, final)
    print(f"\n📏 Cognitive Distance Traveled: {dist:.4f}")
    
    print("\n" + "="*70)
    print("✅ Physics demo completed!")
    print("="*70)
    
    return trajectory, analysis


if __name__ == "__main__":
    demo_physics()
