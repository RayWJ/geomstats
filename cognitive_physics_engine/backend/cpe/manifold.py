"""
CognitiveManifold: 6D Riemannian Manifold for Cognitive Space

This module defines the geometric structure of the cognitive space:
- 3D Hyperbolic Space: (Z-Level, Y-Domain, X-Stance) - hierarchical structure
- 3D Euclidean Space: (W-Intent, T-Time, S-Scale) - linear evolution

The manifold combines these into a 6D product manifold with custom metrics.
"""

import numpy as np
try:
    import geomstats.backend as gs
    from geomstats.geometry.hyperbolic import Hyperbolic
    from geomstats.geometry.euclidean import Euclidean
    GEOMSTATS_AVAILABLE = True
except ImportError:
    GEOMSTATS_AVAILABLE = False
    print("Warning: geomstats not fully available, using simplified implementation")


class CognitiveManifold:
    """
    A 6D Riemannian manifold representing cognitive space.
    
    Dimensions:
    - Z (Level): L1 (facts) → L5 (opinions) [Hyperbolic axis 0]
    - Y (Domain): Tech, Finance, Politics, etc. [Hyperbolic axis 1]
    - X (Stance): Bear (-1) ↔ Bull (+1) [Hyperbolic axis 2]
    - W (Intent): Shadow (-1) ↔ Light (+1) [Euclidean axis 0]
    - T (Time): Past → Future [Euclidean axis 1]
    - S (Scale): Micro → Macro [Euclidean axis 2]
    """
    
    def __init__(self, backend='autograd'):
        """
        Initialize the cognitive manifold.
        
        Args:
            backend: 'numpy', 'autograd', or 'pytorch'
        """
        # Note: In newer geomstats, backend is set via environment variable
        # GEOMSTATS_BACKEND before import, so we just document it here
        # For compatibility, we use numpy backend by default
        
        if GEOMSTATS_AVAILABLE:
            # 1. Spatial manifold: 3D Hyperbolic space
            # Perfect for hierarchical structures (Level hierarchy)
            try:
                self.spatial_manifold = Hyperbolic(dim=3)
            except:
                self.spatial_manifold = None
            
            # 2. Evolution manifold: 3D Euclidean space
            # For linear evolution of Intent, Time, Scale
            try:
                self.evolution_manifold = Euclidean(dim=3)
            except:
                self.evolution_manifold = None
        else:
            self.spatial_manifold = None
            self.evolution_manifold = None
        
        # Dimension mapping for interpretability
        self.dim_names = ['Z_Level', 'Y_Domain', 'X_Stance', 'W_Intent', 'T_Time', 'S_Scale']
        self.spatial_dims = [0, 1, 2]  # Z, Y, X
        self.evolution_dims = [3, 4, 5]  # W, T, S
        
        # For simplified implementation without full geomstats
        self.dim = 6
        
    def metric_matrix(self, point):
        """
        Compute the metric tensor g_ij at a point.
        
        This determines the "geometry" at each point:
        - How distances are measured
        - How gradients flow (friction)
        - Where gravitational wells exist
        
        Args:
            point: 6D coordinate [z, y, x, w, t, s]
            
        Returns:
            6x6 metric tensor matrix
        """
        point = np.array(point)
        
        # Simplified metric: Identity matrix modified by curvature
        # In full implementation, this would use geomstats metrics
        base_metric = np.eye(6)
        
        # Apply cognitive gravity modifier
        cognitive_gravity = self._calculate_gravity(point)
        
        # Scale metric by gravity (higher gravity = harder to move)
        return base_metric * cognitive_gravity
    
    def _calculate_gravity(self, point):
        """
        Calculate "cognitive gravity" at a point.
        
        This function determines which regions of space are:
        - Attractors (low potential, truth sinks)
        - Repellers (high potential, contradiction peaks)
        - Black holes (infinite gravity, logical impossibilities)
        
        Args:
            point: 6D coordinate
            
        Returns:
            Scalar gravity multiplier (1.0 = normal, >1 = heavy, <1 = light)
        """
        z, y, x, w, t, s = point[0], point[1], point[2], point[3], point[4], point[5]
        
        gravity = 1.0
        
        # Level-based gravity: Facts (L1, z~0) have higher gravity
        # Opinions (L5, z~1) have lower gravity
        level_gravity = np.exp(-2.0 * np.abs(z))  # Peak at z=0
        gravity *= (1.0 + 2.0 * level_gravity)
        
        # Intent-based gravity: Shadow regions (w < -0.5) are dangerous
        # Create repulsive force
        if isinstance(w, (int, float)):
            if w < -0.5:
                intent_penalty = np.exp(5.0 * (w + 0.5))  # Exponential barrier
                gravity *= intent_penalty
        else:
            # For array inputs
            shadow_mask = w < -0.5
            intent_penalty = np.where(
                shadow_mask,
                np.exp(5.0 * (w + 0.5)),
                np.ones_like(w)
            )
            gravity *= intent_penalty
        
        return gravity
    
    def random_point(self, n_samples=1):
        """
        Generate random points on the manifold.
        
        Args:
            n_samples: Number of random points to generate
            
        Returns:
            Array of shape (n_samples, 6) or (6,) if n_samples=1
        """
        # Generate random 6D points
        points = np.random.randn(n_samples, 6) * 0.3
        
        # Constrain to valid ranges
        points[:, 0] = np.clip(points[:, 0], 0, 1)  # Z: 0-1
        points[:, 2:] = np.clip(points[:, 2:], -1, 1)  # X,W,T,S: -1 to 1
        
        if n_samples == 1:
            return points[0]
        return points
    
    def project_to_tangent_space(self, vector, base_point):
        """
        Project a vector to the tangent space at base_point.
        
        This ensures vectors respect the manifold's geometry.
        
        Args:
            vector: 6D vector to project
            base_point: 6D point where tangent space is computed
            
        Returns:
            Projected tangent vector
        """
        # Simplified: In full implementation would use manifold's to_tangent
        return np.array(vector)
    
    def exp_map(self, tangent_vec, base_point):
        """
        Exponential map: Move from base_point along tangent_vec.
        
        This is the "correct" way to move on a curved manifold.
        
        Args:
            tangent_vec: Direction and magnitude to move
            base_point: Starting point
            
        Returns:
            New point on manifold
        """
        # Simplified: In full implementation would use manifold's exp
        return np.array(base_point) + np.array(tangent_vec)
    
    def log_map(self, point, base_point):
        """
        Logarithmic map: Compute tangent vector from base_point to point.
        
        Inverse of exponential map.
        
        Args:
            point: Target point
            base_point: Base point
            
        Returns:
            Tangent vector at base_point pointing to point
        """
        # Simplified: In full implementation would use manifold's log
        return np.array(point) - np.array(base_point)
    
    def distance(self, point_a, point_b):
        """
        Compute geodesic distance between two points.
        
        This is the "true" distance respecting manifold curvature.
        
        Args:
            point_a: First point
            point_b: Second point
            
        Returns:
            Geodesic distance (scalar)
        """
        # Simplified: Euclidean distance weighted by metric
        # In full implementation would use manifold's dist
        diff = np.array(point_a) - np.array(point_b)
        return np.linalg.norm(diff)
    
    def geodesic(self, initial_point, end_point, n_steps=100):
        """
        Compute geodesic path between two points.
        
        This is the "shortest path" on the curved manifold.
        
        Args:
            initial_point: Start point
            end_point: End point
            n_steps: Number of interpolation steps
            
        Returns:
            Array of shape (n_steps, 6) representing the path
        """
        t = np.linspace(0.0, 1.0, n_steps)
        initial = np.array(initial_point)
        end = np.array(end_point)
        
        geodesic_points = []
        for t_i in t:
            point = initial + t_i * (end - initial)
            geodesic_points.append(point)
            
        return np.array(geodesic_points)
    
    def interpret_point(self, point):
        """
        Convert a 6D coordinate to human-readable interpretation.
        
        Args:
            point: 6D coordinate
            
        Returns:
            Dictionary with semantic labels
        """
        z, y, x, w, t, s = point
        
        # Level interpretation (L1-L5)
        level_map = {
            (0.0, 0.2): "L1: Verifiable Facts",
            (0.2, 0.4): "L2: Data Analysis", 
            (0.4, 0.6): "L3: Strategic Assessment",
            (0.6, 0.8): "L4: Opinions",
            (0.8, 1.0): "L5: Pure Speculation"
        }
        level_label = next((v for k, v in level_map.items() if k[0] <= abs(float(z)) < k[1]), "Unknown")
        
        # Stance interpretation
        stance_label = "Bullish" if float(x) > 0.1 else ("Bearish" if float(x) < -0.1 else "Neutral")
        
        # Intent interpretation
        intent_label = "Constructive" if float(w) > 0 else "Suspicious"
        
        return {
            "coordinates": point.tolist() if hasattr(point, 'tolist') else list(point),
            "level": level_label,
            "domain_coord": float(y),
            "stance": stance_label,
            "intent": intent_label,
            "time": float(t),
            "scale": float(s)
        }


if __name__ == "__main__":
    # Test the manifold
    print("=== Cognitive Manifold Test ===")
    
    manifold = CognitiveManifold(backend='numpy')
    
    # Generate a random point
    point = manifold.random_point()
    print(f"\nRandom point: {point}")
    print(f"Interpretation: {manifold.interpret_point(point)}")
    
    # Compute metric
    g = manifold.metric_matrix(point)
    print(f"\nMetric matrix shape: {g.shape}")
    
    # Test distance
    point_a = np.array([0.1, 0.0, 0.5, 0.0, 0.0, 0.0])  # L1 fact, bullish
    point_b = np.array([0.8, 0.0, -0.5, 0.0, 0.0, 0.0])  # L5 opinion, bearish
    dist = manifold.distance(point_a, point_b)
    print(f"\nDistance from L1-Bull to L5-Bear: {dist:.4f}")
    
    print("\n✓ Manifold test completed!")
