"""
CognitiveDynamics: Neural ODE-based dynamics on the cognitive manifold

This module defines how "agents" (viewpoints) move on the manifold:
- They are driven by potential energy fields V(x)
- They flow towards Nash equilibria (truth attractors)
- They avoid contradictions (high potential peaks)

Uses torchdiffeq for Neural ODE integration.
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Optional, Tuple, List


class PotentialField(nn.Module):
    """
    Neural network that learns the potential energy landscape V(x).
    
    - Low potential: Truth, consistency, Nash equilibrium
    - High potential: Lies, contradictions, logical impossibility
    """
    
    def __init__(self, manifold_dim=6, hidden_dim=128, n_layers=3):
        super().__init__()
        
        layers = []
        layers.append(nn.Linear(manifold_dim, hidden_dim))
        layers.append(nn.Tanh())
        
        for _ in range(n_layers - 1):
            layers.append(nn.Linear(hidden_dim, hidden_dim))
            layers.append(nn.Tanh())
            
        layers.append(nn.Linear(hidden_dim, 1))
        
        self.network = nn.Sequential(*layers)
        
        # Initialize with small weights for stable gradients
        for layer in self.network:
            if isinstance(layer, nn.Linear):
                nn.init.xavier_normal_(layer.weight, gain=0.1)
                nn.init.zeros_(layer.bias)
    
    def forward(self, state):
        """
        Compute potential energy at state.
        
        Args:
            state: (batch_size, 6) or (6,) tensor of positions
            
        Returns:
            potential: (batch_size, 1) or scalar tensor
        """
        if state.dim() == 1:
            state = state.unsqueeze(0)
            result = self.network(state)
            return result.squeeze(0)
        return self.network(state)


class CognitiveDynamics(nn.Module):
    """
    Defines the ODE governing agent movement on the cognitive manifold:
    
        dx/dt = -∇V(x) - friction * v
        
    Where:
    - ∇V(x) is the gradient of potential (drives towards low energy)
    - friction damps oscillations
    - The gradient is Riemannian (respects manifold curvature)
    """
    
    def __init__(
        self, 
        manifold,
        hidden_dim: int = 128,
        n_layers: int = 3,
        friction: float = 0.1,
        use_riemannian_gradient: bool = True
    ):
        """
        Initialize dynamics module.
        
        Args:
            manifold: CognitiveManifold instance
            hidden_dim: Hidden layer size for potential network
            n_layers: Number of layers in potential network
            friction: Friction coefficient (damping)
            use_riemannian_gradient: Use Riemannian gradients (recommended)
        """
        super().__init__()
        
        self.manifold = manifold
        self.potential_net = PotentialField(
            manifold_dim=6,
            hidden_dim=hidden_dim,
            n_layers=n_layers
        )
        self.friction = friction
        self.use_riemannian_gradient = use_riemannian_gradient
        
        # Storage for trajectory analysis
        self.trajectory_history = []
        
    def forward(self, t, state):
        """
        Compute dx/dt for the ODE solver.
        
        This defines the "physics" of how viewpoints move.
        
        Args:
            t: Current time (scalar)
            state: Current position (batch_size, 6) or (6,)
            
        Returns:
            velocity: dx/dt (same shape as state)
        """
        # Ensure state requires gradient
        if not state.requires_grad:
            state = state.requires_grad_(True)
        
        # Compute potential energy
        V = self.potential_net(state)
        
        # Compute gradient ∇V
        grad_outputs = torch.ones_like(V)
        grad_V = torch.autograd.grad(
            outputs=V,
            inputs=state,
            grad_outputs=grad_outputs,
            create_graph=True,
            retain_graph=True
        )[0]
        
        if self.use_riemannian_gradient:
            # Convert Euclidean gradient to Riemannian gradient
            # ∇_R V = g^{-1} ∇_E V
            grad_V = self._to_riemannian_gradient(grad_V, state)
        
        # Compute velocity: dx/dt = -∇V - friction * v
        # For first-order dynamics, velocity = -∇V
        velocity = -grad_V
        
        # Optional: Add friction if using second-order dynamics
        # This would require state = [position, velocity]
        
        return velocity
    
    def _to_riemannian_gradient(self, euclidean_grad, base_point):
        """
        Convert Euclidean gradient to Riemannian gradient.
        
        In curved space, gradients must be modified by the metric tensor:
        ∇_R = g^{-1} ∇_E
        
        Args:
            euclidean_grad: Standard gradient (batch_size, 6)
            base_point: Point where gradient is computed (batch_size, 6)
            
        Returns:
            Riemannian gradient (batch_size, 6)
        """
        # Get metric tensor at base_point
        # Note: This requires converting between torch and geomstats
        
        if euclidean_grad.dim() == 1:
            # Single point
            g = torch.from_numpy(
                np.array(self.manifold.metric_matrix(base_point.detach().cpu().numpy()))
            ).float().to(euclidean_grad.device)
            
            # Compute g^{-1} * grad
            try:
                g_inv = torch.inverse(g)
                riem_grad = torch.matmul(g_inv, euclidean_grad.unsqueeze(-1)).squeeze(-1)
            except:
                # If singular, use pseudo-inverse
                g_inv = torch.pinverse(g)
                riem_grad = torch.matmul(g_inv, euclidean_grad.unsqueeze(-1)).squeeze(-1)
                
            return riem_grad
        else:
            # Batch of points
            batch_size = euclidean_grad.shape[0]
            riem_grads = []
            
            for i in range(batch_size):
                g = torch.from_numpy(
                    np.array(self.manifold.metric_matrix(base_point[i].detach().cpu().numpy()))
                ).float().to(euclidean_grad.device)
                
                try:
                    g_inv = torch.inverse(g)
                    riem_grad = torch.matmul(g_inv, euclidean_grad[i].unsqueeze(-1)).squeeze(-1)
                except:
                    g_inv = torch.pinverse(g)
                    riem_grad = torch.matmul(g_inv, euclidean_grad[i].unsqueeze(-1)).squeeze(-1)
                    
                riem_grads.append(riem_grad)
                
            return torch.stack(riem_grads)
    
    def simulate_collapse(
        self,
        initial_points: torch.Tensor,
        T: float = 10.0,
        method: str = 'euler',
        dt: float = 0.1,
        return_trajectory: bool = False
    ) -> Tuple[torch.Tensor, Optional[List[torch.Tensor]]]:
        """
        Simulate the collapse of multiple viewpoints towards equilibrium.
        
        This is the core "physics simulation" where:
        1. Start with N diverse viewpoints (initial_points)
        2. Let them flow under the potential field
        3. Watch them converge to Nash equilibria (truth attractors)
        
        Args:
            initial_points: (N, 6) tensor of starting positions
            T: Total simulation time
            method: 'euler', 'rk4', or 'dopri5'
            dt: Time step for integration
            return_trajectory: Return full trajectory history
            
        Returns:
            final_points: (N, 6) tensor of final positions
            trajectory: Optional list of intermediate states
        """
        self.trajectory_history = []
        
        current_state = initial_points.clone().detach().requires_grad_(True)
        trajectory = [current_state.detach().clone()]
        
        if method == 'euler':
            # Simple Euler integration
            n_steps = int(T / dt)
            t = 0.0
            
            for step in range(n_steps):
                with torch.enable_grad():
                    velocity = self.forward(t, current_state)
                
                current_state = current_state.detach() + dt * velocity.detach()
                current_state = current_state.requires_grad_(True)
                
                t += dt
                
                if return_trajectory:
                    trajectory.append(current_state.detach().clone())
                    
        elif method == 'rk4':
            # Runge-Kutta 4th order
            n_steps = int(T / dt)
            t = 0.0
            
            for step in range(n_steps):
                with torch.enable_grad():
                    k1 = self.forward(t, current_state)
                    
                state_k2 = (current_state.detach() + 0.5 * dt * k1.detach()).requires_grad_(True)
                with torch.enable_grad():
                    k2 = self.forward(t + 0.5 * dt, state_k2)
                
                state_k3 = (current_state.detach() + 0.5 * dt * k2.detach()).requires_grad_(True)
                with torch.enable_grad():
                    k3 = self.forward(t + 0.5 * dt, state_k3)
                
                state_k4 = (current_state.detach() + dt * k3.detach()).requires_grad_(True)
                with torch.enable_grad():
                    k4 = self.forward(t + dt, state_k4)
                
                current_state = current_state.detach() + (dt / 6.0) * (
                    k1.detach() + 2*k2.detach() + 2*k3.detach() + k4.detach()
                )
                current_state = current_state.requires_grad_(True)
                
                t += dt
                
                if return_trajectory:
                    trajectory.append(current_state.detach().clone())
                    
        else:
            raise ValueError(f"Unknown integration method: {method}")
        
        self.trajectory_history = trajectory
        
        if return_trajectory:
            return current_state.detach(), trajectory
        else:
            return current_state.detach(), None
    
    def add_potential_barrier(
        self,
        center: torch.Tensor,
        height: float = 100.0,
        width: float = 0.5
    ):
        """
        Dynamically add a Gaussian potential barrier to the field.
        
        This allows injecting new information (e.g., breaking news)
        that creates repulsive forces in certain regions.
        
        Args:
            center: 6D position of barrier center
            height: Peak height of barrier
            width: Width of Gaussian (smaller = sharper peak)
        """
        # This would modify the potential network
        # For now, we store barriers and compute them explicitly
        if not hasattr(self, 'barriers'):
            self.barriers = []
            
        self.barriers.append({
            'center': center,
            'height': height,
            'width': width
        })
    
    def compute_total_potential(self, state):
        """
        Compute total potential including learned field + barriers.
        
        Args:
            state: (batch_size, 6) or (6,) positions
            
        Returns:
            Total potential energy
        """
        V_learned = self.potential_net(state)
        
        if not hasattr(self, 'barriers') or len(self.barriers) == 0:
            return V_learned
        
        # Add Gaussian barriers
        V_barriers = 0
        for barrier in self.barriers:
            center = barrier['center'].to(state.device)
            diff = state - center
            dist_sq = (diff ** 2).sum(dim=-1, keepdim=True)
            V_barrier = barrier['height'] * torch.exp(-dist_sq / (2 * barrier['width']**2))
            V_barriers = V_barriers + V_barrier
            
        return V_learned + V_barriers
    
    def analyze_equilibrium(self, points: torch.Tensor, threshold: float = 0.5):
        """
        Analyze final points to identify equilibrium clusters.
        
        Args:
            points: (N, 6) final positions
            threshold: Distance threshold for clustering
            
        Returns:
            Dictionary with cluster analysis
        """
        # Simple clustering based on distance
        N = points.shape[0]
        clusters = []
        assigned = [False] * N
        
        for i in range(N):
            if assigned[i]:
                continue
                
            cluster = [i]
            assigned[i] = True
            
            for j in range(i+1, N):
                if assigned[j]:
                    continue
                    
                dist = torch.norm(points[i] - points[j]).item()
                if dist < threshold:
                    cluster.append(j)
                    assigned[j] = True
                    
            clusters.append(cluster)
        
        # Compute cluster statistics
        cluster_info = []
        for cluster in clusters:
            cluster_points = points[cluster]
            centroid = cluster_points.mean(dim=0)
            
            cluster_info.append({
                'size': len(cluster),
                'centroid': centroid.cpu().numpy(),
                'indices': cluster
            })
        
        return {
            'n_clusters': len(clusters),
            'clusters': cluster_info
        }


if __name__ == "__main__":
    print("=== Cognitive Dynamics Test ===")
    
    # Import manifold
    import sys
    sys.path.append('..')
    from manifold import CognitiveManifold
    
    manifold = CognitiveManifold(backend='numpy')
    dynamics = CognitiveDynamics(manifold, hidden_dim=64, n_layers=2)
    
    # Generate random initial viewpoints
    N = 100
    initial_points = torch.randn(N, 6) * 0.3  # Small random positions
    
    print(f"\nSimulating collapse of {N} viewpoints...")
    final_points, _ = dynamics.simulate_collapse(
        initial_points,
        T=5.0,
        method='euler',
        dt=0.1
    )
    
    print(f"Initial spread: {initial_points.std(dim=0).mean():.4f}")
    print(f"Final spread: {final_points.std(dim=0).mean():.4f}")
    
    # Analyze equilibria
    analysis = dynamics.analyze_equilibrium(final_points, threshold=0.5)
    print(f"\nFound {analysis['n_clusters']} equilibrium clusters")
    for i, cluster in enumerate(analysis['clusters']):
        print(f"  Cluster {i+1}: {cluster['size']} points")
    
    print("\n✓ Dynamics test completed!")
