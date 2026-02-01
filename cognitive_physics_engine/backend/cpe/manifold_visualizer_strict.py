"""
3D Manifold Visualization for Strict Mathematical Implementation
=================================================================

This script generates enhanced visualizations for the strict Raywu manifold,
showing:
1. Poincaré Disk (Hyperbolic space H²)
2. Circle topology (S¹)
3. Metric warping (shadow effect)
4. Agent trajectories on the manifold
5. Geodesic paths (curved, not straight!)
"""

import numpy as np
import json
from pathlib import Path

# Import strict manifold
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from cpe.raywu_manifold_strict import RaywuManifold
    STRICT_AVAILABLE = True
except ImportError:
    try:
        from raywu_manifold_strict import RaywuManifold
        STRICT_AVAILABLE = True
    except ImportError:
        STRICT_AVAILABLE = False
        print("⚠️  Strict manifold not available, using simplified version")
        try:
            from cpe.raywu_manifold import RaywuCognitiveManifold as RaywuManifold
        except ImportError:
            from raywu_manifold import RaywuCognitiveManifold as RaywuManifold


def generate_poincare_grid(n_circles=10, n_rays=16):
    """Generate Poincaré disk grid."""
    grid_data = {
        'circles': [],
        'rays': []
    }
    
    # Concentric circles
    for i in range(1, n_circles + 1):
        r = i / n_circles * 0.95  # Stay inside unit disk
        theta = np.linspace(0, 2*np.pi, 100)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        grid_data['circles'].append({
            'radius': r,
            'points': [[float(x[j]), float(y[j])] for j in range(len(x))]
        })
    
    # Radial rays
    for i in range(n_rays):
        theta = i * 2 * np.pi / n_rays
        t = np.linspace(0, 0.95, 50)
        x = t * np.cos(theta)
        y = t * np.sin(theta)
        grid_data['rays'].append({
            'angle': float(theta),
            'points': [[float(x[j]), float(y[j])] for j in range(len(x))]
        })
    
    return grid_data


def generate_circle_topology(n_points=50):
    """Generate circle (S¹) topology."""
    theta = np.linspace(0, 2*np.pi, n_points)
    x = np.cos(theta)
    y = np.sin(theta)
    
    return {
        'points': [[float(x[i]), float(y[i])] for i in range(n_points)]
    }


def generate_agents_on_manifold(manifold, n_agents=7):
    """Generate random agents on the strict manifold."""
    agents_data = []
    
    configs = [
        ("L1 Finance Bear", 1, 'finance', -0.7, 0.9, 0.0, -0.8),
        ("L5 Tech Bull", 5, 'tech', 0.9, -0.8, 0.8, 0.9),
        ("L3 Politics Neutral", 3, 'politics', 0.0, 0.1, 0.0, 0.0),
        ("L2 Science Bear", 2, 'science', -0.5, 0.6, -0.3, -0.2),
        ("L4 Healthcare Bull", 4, 'healthcare', 0.6, -0.3, 0.5, 0.6),
        ("L5 Energy Shadow", 5, 'energy', 0.3, -0.9, 0.2, 0.5),
        ("L1 Tech Constructive", 1, 'tech', 0.4, 0.95, -0.5, -0.9),
    ]
    
    for name, *params in configs:
        point = manifold.encode_agent_state(*params)
        decoded = manifold.decode_agent_state(point)
        
        # Extract coordinates
        z1, z2 = point[0], point[1]
        y1, y2 = point[2], point[3]
        x, w, t = point[4], point[5], point[6]
        
        # Compute metric determinant at this point
        g = manifold.metric.metric_matrix(point)
        det_g = np.linalg.det(g)
        
        agents_data.append({
            'name': name,
            'position': {
                'hyperbolic': [float(z1), float(z2)],
                'circle': [float(y1), float(y2)],
                'euclidean': [float(x), float(w), float(t)]
            },
            'decoded': decoded,
            'metrics': {
                'det_g': float(det_g),
                'hyperbolic_radius': float(np.sqrt(z1**2 + z2**2)),
                'circle_angle': float(np.arctan2(y2, y1))
            }
        })
    
    return agents_data


def generate_geodesics(manifold, agents_data, n_steps=20):
    """Generate geodesic paths between agents."""
    geodesics = []
    
    # Select a few interesting pairs
    pairs = [
        (0, 1),  # L1 Bear ↔ L5 Bull (maximal distance)
        (2, 4),  # L3 Neutral ↔ L4 Bull
        (5, 6),  # L5 Shadow ↔ L1 Constructive
    ]
    
    for i, j in pairs:
        agent_a = agents_data[i]
        agent_b = agents_data[j]
        
        # Reconstruct full points (7D)
        point_a = np.array(
            agent_a['position']['hyperbolic'] +
            agent_a['position']['circle'] +
            agent_a['position']['euclidean']
        )
        point_b = np.array(
            agent_b['position']['hyperbolic'] +
            agent_b['position']['circle'] +
            agent_b['position']['euclidean']
        )
        
        # Compute geodesic distance
        dist = manifold.cognitive_distance(point_a, point_b)
        
        # Generate geodesic path (simplified: linear interpolation in ambient space)
        # TODO: Use proper geodesic flow via exp map
        path = []
        for t in np.linspace(0, 1, n_steps):
            point_t = (1 - t) * point_a + t * point_b
            
            # Extract hyperbolic coords
            z1, z2 = point_t[0], point_t[1]
            
            path.append([float(z1), float(z2)])
        
        geodesics.append({
            'from': agent_a['name'],
            'to': agent_b['name'],
            'distance': float(dist),
            'path': path
        })
    
    return geodesics


def generate_metric_heatmap(manifold, grid_size=30):
    """Generate metric determinant heatmap in Poincaré disk."""
    heatmap = []
    
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            # Map to Poincaré disk coordinates
            x = (i / grid_size - 0.5) * 1.8  # -0.9 to 0.9
            y = (j / grid_size - 0.5) * 1.8
            
            r = np.sqrt(x**2 + y**2)
            if r >= 0.95:
                row.append(None)  # Outside disk
                continue
            
            # Create a test point (set other coords to neutral values)
            point = np.array([x, y, 1.0, 0.0, 0.0, 0.0, 0.0])
            
            # Compute metric determinant
            g = manifold.metric.metric_matrix(point)
            det_g = np.linalg.det(g)
            
            row.append(float(np.log10(max(det_g, 1e-10))))  # Log scale
        
        heatmap.append(row)
    
    return heatmap


def main():
    print("\n" + "="*70)
    print("🎨 GENERATING STRICT MANIFOLD VISUALIZATION DATA")
    print("="*70 + "\n")
    
    # Initialize manifold
    if STRICT_AVAILABLE:
        manifold = RaywuManifold(warp_strength=100.0)
        print("✓ Using STRICT mathematical implementation")
    else:
        manifold = RaywuManifold()
        print("✓ Using simplified implementation")
    
    print()
    
    # Generate visualization data
    data = {}
    
    print("Generating Poincaré disk grid...")
    data['poincare_grid'] = generate_poincare_grid(n_circles=8, n_rays=16)
    print(f"  ✓ {len(data['poincare_grid']['circles'])} circles, {len(data['poincare_grid']['rays'])} rays")
    
    print("Generating circle topology...")
    data['circle_topology'] = generate_circle_topology(n_points=50)
    print(f"  ✓ {len(data['circle_topology']['points'])} points")
    
    print("Generating agents on manifold...")
    data['agents'] = generate_agents_on_manifold(manifold, n_agents=7)
    print(f"  ✓ {len(data['agents'])} agents")
    for agent in data['agents']:
        print(f"    - {agent['name']}: det(g)={agent['metrics']['det_g']:.2e}")
    
    print("Generating geodesic paths...")
    data['geodesics'] = generate_geodesics(manifold, data['agents'], n_steps=20)
    print(f"  ✓ {len(data['geodesics'])} geodesics")
    for geo in data['geodesics']:
        print(f"    - {geo['from']} ↔ {geo['to']}: distance={geo['distance']:.4f}")
    
    print("Generating metric heatmap...")
    data['metric_heatmap'] = generate_metric_heatmap(manifold, grid_size=30)
    print(f"  ✓ {len(data['metric_heatmap'])}×{len(data['metric_heatmap'][0])} grid")
    
    # Add metadata
    data['metadata'] = {
        'implementation': 'strict' if STRICT_AVAILABLE else 'simplified',
        'warp_strength': 100.0 if STRICT_AVAILABLE else 'N/A',
        'manifold_structure': 'H²×S¹×R³' if STRICT_AVAILABLE else 'Fake 9D',
        'timestamp': '2026-02-01'
    }
    
    # Save to file
    output_path = Path(__file__).parent / 'visualization_data_strict.json'
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Data saved to: {output_path}")
    print(f"  File size: {output_path.stat().st_size / 1024:.2f} KB")
    
    print("\n" + "="*70)
    print("✅ Visualization data generation completed!")
    print("="*70)
    print("\nNext steps:")
    print("  1. Open frontend: http://localhost:8000/viz")
    print("  2. Or use: python -m http.server 8000")
    print("  3. Load visualization_data_strict.json")
    print()


if __name__ == "__main__":
    main()
