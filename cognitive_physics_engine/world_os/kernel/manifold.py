"""
Cognitive Manifold - The Physical Stage
========================================

This module defines the true Riemannian manifold where cognitive entities live.

Philosophy:
- Hierarchy (Z): Hyperbolic space H³ (exponential capacity)
- Domain (Y): Spherical space S² (periodic structure)
- Attributes (X,W,T,S): Euclidean space Rⁿ (linear properties)

Mathematical Structure:
    M = H³ × S² × Rⁿ
    
The manifold has a custom Riemannian metric that encodes:
- Friction (resistance to movement)
- Shadow gravity (hidden agenda effects)
- Level-based warping (L1 facts vs L5 speculation)

Author: Raywu WorldOS Team
Date: 2026-02-01
Version: v61.0 - Ultimate Implementation
"""

import numpy as np
from typing import Optional

try:
    import jax
    import jax.numpy as jnp
    JAX_AVAILABLE = True
except ImportError:
    JAX_AVAILABLE = False
    # Fallback to NumPy
    jnp = np
    print("⚠️  JAX not available. Using NumPy fallback (slower).")

try:
    import geomstats.backend as gs
    from geomstats.geometry.hyperbolic import Hyperbolic
    from geomstats.geometry.hypersphere import Hypersphere
    from geomstats.geometry.euclidean import Euclidean
    from geomstats.geometry.product_manifold import ProductManifold
    from geomstats.geometry.riemannian_metric import RiemannianMetric
    GEOMSTATS_AVAILABLE = True
except ImportError:
    GEOMSTATS_AVAILABLE = False
    raise ImportError("❌ Geomstats is REQUIRED for manifold implementation!")


class CognitiveFrictionMap:
    """
    Friction Map - The Physics of Information Resistance
    
    This class represents the "terrain" of cognitive space.
    High friction = hard to move (e.g., deeply held beliefs, L1 facts)
    Low friction = easy to drift (e.g., L5 speculation, weak signals)
    """
    
    def __init__(self):
        """Initialize empty friction map."""
        self.friction_sources = []  # List of (position, strength) pairs
    
    def add_source(self, position: np.ndarray, strength: float, radius: float = 1.0):
        """
        Add a friction source (e.g., a "sticky" fact or narrative).
        
        Args:
            position: 6D coordinates of the source
            strength: How strong the friction is (0-1)
            radius: Effective radius of influence
        """
        self.friction_sources.append({
            'position': np.array(position),
            'strength': strength,
            'radius': radius
        })
    
    def get_friction_at(self, point: np.ndarray) -> float:
        """
        Compute total friction at a given point.
        
        Uses Gaussian falloff: f(r) = strength * exp(-r²/(2*radius²))
        """
        total_friction = 0.0
        
        for source in self.friction_sources:
            # Compute distance (Euclidean for now, should be geodesic ideally)
            diff = point - source['position']
            dist_sq = np.sum(diff ** 2)
            
            # Gaussian falloff
            friction = source['strength'] * np.exp(-dist_sq / (2 * source['radius']**2))
            total_friction += friction
        
        return total_friction


class CognitiveMetric(RiemannianMetric):
    """
    Custom Riemannian Metric with Friction and Shadow Warping
    
    This is the core physics: the metric g_ij(x) encodes how hard it is
    to move in different directions at different locations.
    
    Key Features:
    1. Base metric from product structure (H³ × S² × Rⁿ)
    2. Friction warping (terrain-dependent resistance)
    3. Shadow gravity (W-axis creates black holes)
    4. Level-based scaling (L1 sticky, L5 fluid)
    """
    
    def __init__(self, base_manifold, friction_map: CognitiveFrictionMap):
        """
        Args:
            base_manifold: ProductManifold instance
            friction_map: FrictionMap defining terrain
        """
        self.base_manifold = base_manifold
        self.friction_map = friction_map
        
        # Dimension breakdown
        self.dim_h = 3  # Hyperbolic (Z-axis hierarchy)
        self.dim_s = 3  # Sphere embedding (Y-axis domain, intrinsic dim=2)
        self.dim_e = 4  # Euclidean (X, W, T, S)
        self.dim = self.dim_h + self.dim_s + self.dim_e  # Total: 10D embedding
        
        super().__init__(space=base_manifold)
    
    def _base_metric_matrix(self, base_point: np.ndarray) -> np.ndarray:
        """
        Compute base metric from product structure.
        
        For M₁ × M₂ × M₃, the metric is block-diagonal:
            g = diag(g_H, g_S, g_E)
        """
        g_base = np.eye(self.dim)
        
        # Extract coordinates
        h_coords = base_point[:self.dim_h]  # Hyperbolic
        s_coords = base_point[self.dim_h:self.dim_h+self.dim_s]  # Sphere
        # e_coords = base_point[self.dim_h+self.dim_s:]  # Euclidean (flat, identity)
        
        # 1. Hyperbolic metric (Poincaré ball model)
        # g_H = (4 / (1 - ||x||²)²) * I
        h_norm_sq = np.dot(h_coords, h_coords)
        h_norm_sq = np.clip(h_norm_sq, 0, 0.99)  # Stay in ball
        hyperbolic_factor = 4.0 / ((1.0 - h_norm_sq) ** 2)
        g_base[:self.dim_h, :self.dim_h] *= hyperbolic_factor
        
        # 2. Sphere metric (induced from ambient Euclidean)
        # g_S = I - outer(x, x) for unit sphere
        s_norm = np.linalg.norm(s_coords)
        if s_norm > 1e-6:
            s_unit = s_coords / s_norm
            sphere_proj = np.eye(self.dim_s) - np.outer(s_unit, s_unit)
            g_base[self.dim_h:self.dim_h+self.dim_s, 
                   self.dim_h:self.dim_h+self.dim_s] = sphere_proj
        
        # 3. Euclidean metric (already identity)
        
        return g_base
    
    def metric_matrix(self, base_point: np.ndarray) -> np.ndarray:
        """
        Full metric with friction and shadow warping.
        
        g(x) = g_base(x) * (1 + friction(x)) * shadow_warp(w)
        
        Self-Verification:
        - Friction term makes g larger → distances increase → movement harder
        - Shadow term creates singularities (black holes) for hidden agendas
        """
        base_point = np.array(base_point)
        
        # 1. Base metric from geometry
        g_base = self._base_metric_matrix(base_point)
        
        # 2. Friction warping
        friction = self.friction_map.get_friction_at(base_point)
        friction_factor = 1.0 + 5.0 * friction  # Amplify effect
        
        # 3. Shadow warping (W-axis effect) - WITH NUMERICAL STABILITY
        w_idx = self.dim_h + self.dim_s + 1  # Index of W coordinate
        if len(base_point) > w_idx:
            w_value = base_point[w_idx]
            # Shadow (w < 0) creates strong warping
            # But cap at reasonable level to avoid overflow
            if w_value < -0.3:
                exponent = min(10.0 * abs(w_value + 0.3), 20.0)  # Cap at 20
                shadow_factor = np.exp(exponent)
            else:
                shadow_factor = 1.0
        else:
            shadow_factor = 1.0
        
        # 4. Level-based scaling
        # L1 (near boundary of hyperbolic) = high friction
        # L5 (near center) = low friction
        h_coords = base_point[:self.dim_h]
        h_radius = np.linalg.norm(h_coords)
        level_factor = 1.0 + 2.0 * h_radius  # More friction near boundary
        
        # 5. Combine all warping
        total_warp = friction_factor * shadow_factor * level_factor
        
        g_warped = g_base * total_warp
        
        # 6. Ensure positive definiteness
        g_warped = g_warped + 1e-6 * np.eye(self.dim)
        
        return g_warped
    
    def inner_product(self, tangent_vec_a, tangent_vec_b, base_point):
        """Inner product: <u, v>_g = u^T g(x) v"""
        g = self.metric_matrix(base_point)
        return float(np.dot(tangent_vec_a, np.dot(g, tangent_vec_b)))
    
    def squared_norm(self, vector, base_point):
        """Squared norm: ||v||²_g"""
        return self.inner_product(vector, vector, base_point)
    
    def norm(self, vector, base_point):
        """Norm: ||v||_g"""
        return np.sqrt(max(self.squared_norm(vector, base_point), 0))
    
    def dist(self, point_a, point_b):
        """
        Geodesic distance (approximation via midpoint metric).
        
        True geodesic would require solving ODE, but midpoint gives good estimate.
        """
        point_a = np.array(point_a)
        point_b = np.array(point_b)
        
        midpoint = (point_a + point_b) / 2.0
        g = self.metric_matrix(midpoint)
        
        diff = point_b - point_a
        dist_sq = np.dot(diff, np.dot(g, diff))
        dist_sq = max(dist_sq, 0)  # Numerical safety
        
        return np.sqrt(dist_sq)


class CognitiveManifold:
    """
    The Complete Cognitive Manifold: M = H³ × S² × R⁴
    
    This is the stage where all cognitive physics happens.
    
    Structure:
    - H³: Hyperbolic space for hierarchy (Z-axis)
    - S²: Spherical space for domains (Y-axis)
    - R⁴: Euclidean space for attributes (X, W, T, S)
    
    Total: 10D embedding, 9D intrinsic
    """
    
    def __init__(self, friction_map: Optional[CognitiveFrictionMap] = None):
        """
        Initialize the manifold with optional friction map.
        
        Args:
            friction_map: Optional terrain definition
        """
        if not GEOMSTATS_AVAILABLE:
            raise RuntimeError("Geomstats required!")
        
        # Create sub-manifolds
        self.hyperbolic_space = Hyperbolic(dim=3, coords_type='ball')
        self.sphere_space = Hypersphere(dim=2)  # Embedded in R³
        self.euclidean_space = Euclidean(dim=4)
        
        # Create product manifold
        self.manifold = ProductManifold(
            factors=[self.hyperbolic_space, self.sphere_space, self.euclidean_space]
        )
        
        # Create friction map
        if friction_map is None:
            friction_map = CognitiveFrictionMap()
        self.friction_map = friction_map
        
        # Create custom metric
        self.metric = CognitiveMetric(self.manifold, self.friction_map)
        
        # Dimensions
        self.dim_embedding = 10  # 3 + 3 + 4
        self.dim_intrinsic = 9   # 3 + 2 + 4
        
        print(f"✓ CognitiveManifold initialized")
        print(f"  Structure: H³ × S² × R⁴")
        print(f"  Embedding: {self.dim_embedding}D")
        print(f"  Intrinsic: {self.dim_intrinsic}D")
    
    def encode_state(self, level: int, domain: str, stance: float, 
                     intent: float, time: float, scale: float) -> np.ndarray:
        """
        Encode semantic state → manifold coordinates.
        
        Args:
            level: 1-5 (L1=Facts, L5=Speculation)
            domain: Domain identifier
            stance: -1 (bear) to +1 (bull)
            intent: -1 (shadow) to +1 (light)
            time: -1 (past) to +1 (future)
            scale: -1 (micro) to +1 (macro)
        
        Returns:
            10D point on manifold
        """
        # 1. Z-axis → Hyperbolic (3D)
        # L5 (speculation) → center (r=0)
        # L1 (facts) → boundary (r→1)
        level_normalized = (level - 1) / 4.0  # 0 to 1
        h_radius = level_normalized * 0.85  # Stay inside ball
        
        # Use scale for angular components
        h_theta = (scale + 1) * np.pi
        h_phi = (stance + 1) * np.pi / 2
        
        h1 = h_radius * np.sin(h_theta) * np.cos(h_phi)
        h2 = h_radius * np.sin(h_theta) * np.sin(h_phi)
        h3 = h_radius * np.cos(h_theta)
        
        # 2. Y-axis → Sphere (3D embedding)
        domain_map = {
            'tech': 0, 'finance': 1, 'politics': 2,
            'science': 3, 'healthcare': 4, 'energy': 5
        }
        domain_idx = domain_map.get(domain.lower(), 0)
        
        s_theta = (domain_idx % 6) * (2 * np.pi / 6)
        s_phi = np.pi / 2
        
        s1 = np.sin(s_phi) * np.cos(s_theta)
        s2 = np.sin(s_phi) * np.sin(s_theta)
        s3 = np.cos(s_phi)
        
        # 3. X, W, T, S → Euclidean (4D)
        x = np.clip(stance, -1, 1)
        w = np.clip(intent, -1, 1)
        t = np.clip(time, -1, 1)
        s = np.clip(scale, -1, 1)
        
        # Combine into 10D point
        point = np.array([h1, h2, h3, s1, s2, s3, x, w, t, s])
        
        return point
    
    def decode_state(self, point: np.ndarray) -> dict:
        """
        Decode manifold coordinates → semantic state.
        """
        h1, h2, h3 = point[0], point[1], point[2]
        s1, s2, s3 = point[3], point[4], point[5]
        x, w, t, s = point[6], point[7], point[8], point[9]
        
        # Decode level from hyperbolic radius
        h_radius = np.sqrt(h1**2 + h2**2 + h3**2)
        level = 1 + int(h_radius / 0.85 * 4)
        level = np.clip(level, 1, 5)
        
        # Decode domain from sphere position
        s_theta = np.arctan2(s2, s1)
        if s_theta < 0:
            s_theta += 2 * np.pi
        domain_idx = int(s_theta / (2 * np.pi / 6))
        domain_names = ['tech', 'finance', 'politics', 'science', 'healthcare', 'energy']
        domain = domain_names[domain_idx % 6]
        
        return {
            'level': f'L{level}',
            'domain': domain,
            'stance': 'bullish' if x > 0.3 else ('bearish' if x < -0.3 else 'neutral'),
            'intent': 'constructive' if w > 0 else 'shadow',
            'time_focus': 'future' if t > 0.3 else ('past' if t < -0.3 else 'present'),
            'scale': 'macro' if s > 0.3 else ('micro' if s < -0.3 else 'meso'),
            'coordinates': point.tolist()
        }
    
    def cognitive_distance(self, point_a: np.ndarray, point_b: np.ndarray) -> float:
        """
        Compute cognitive distance using custom metric.
        
        This respects friction, shadow, and manifold curvature.
        """
        return self.metric.dist(point_a, point_b)


# ============================================================================
# VALIDATION
# ============================================================================

def validate_manifold():
    """Test the manifold implementation."""
    print("\n" + "="*70)
    print("🧪 VALIDATING COGNITIVE MANIFOLD")
    print("="*70 + "\n")
    
    # Create manifold with friction
    friction_map = CognitiveFrictionMap()
    # Add a "sticky" fact at L1
    friction_map.add_source(
        position=np.array([0.8, 0, 0, 1, 0, 0, 0.5, 0.9, 0, -0.5]),
        strength=0.8,
        radius=0.5
    )
    
    manifold = CognitiveManifold(friction_map=friction_map)
    
    # Test encoding
    point_a = manifold.encode_state(
        level=1, domain='tech', stance=0.7, intent=0.9, time=0.0, scale=-0.5
    )
    point_b = manifold.encode_state(
        level=5, domain='finance', stance=-0.7, intent=-0.9, time=0.5, scale=0.8
    )
    
    print("Point A (L1 Tech Bull, Light):")
    print(f"  Coordinates: {point_a}")
    
    print("\nPoint B (L5 Finance Bear, Shadow):")
    print(f"  Coordinates: {point_b}")
    
    # Test distance
    dist = manifold.cognitive_distance(point_a, point_b)
    print(f"\n📏 Cognitive Distance: {dist:.4f}")
    
    # Test metric at different points
    g_a = manifold.metric.metric_matrix(point_a)
    g_b = manifold.metric.metric_matrix(point_b)
    
    det_a = np.linalg.det(g_a)
    det_b = np.linalg.det(g_b)
    
    print(f"\n📐 Metric Determinants:")
    print(f"  det(g) at A (L1, Light): {det_a:.2e}")
    print(f"  det(g) at B (L5, Shadow): {det_b:.2e}")
    print(f"  Distortion ratio: {det_b/det_a:.2e}x")
    
    print("\n" + "="*70)
    print("✅ Manifold validation completed!")
    print("="*70)


if __name__ == "__main__":
    validate_manifold()
