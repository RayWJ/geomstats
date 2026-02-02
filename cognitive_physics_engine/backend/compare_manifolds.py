"""
COMPARATIVE DEMO: Strict vs Simplified Raywu Manifold
======================================================

This script demonstrates the difference between:
1. Strict Mathematical Implementation (TRUE differential geometry)
2. Simplified Engineering Implementation (Fast approximation)

Run this to see side-by-side validation results.
"""

import numpy as np
import sys
import time

print("\n" + "="*80)
print("🔬 COMPARATIVE DEMO: STRICT vs SIMPLIFIED RAYWU MANIFOLD")
print("="*80 + "\n")

# ============================================================================
# PART 1: Strict Mathematical Implementation
# ============================================================================

print("╔" + "═"*78 + "╗")
print("║" + " "*20 + "STRICT MATHEMATICAL IMPLEMENTATION" + " "*24 + "║")
print("╚" + "═"*78 + "╝\n")

try:
    from cpe.raywu_manifold_strict import RaywuManifold as StrictManifold
    
    strict_start = time.time()
    strict_manifold = StrictManifold(warp_strength=100.0)
    strict_init_time = time.time() - strict_start
    
    print(f"✓ Strict manifold initialized in {strict_init_time*1000:.2f}ms\n")
    
    # Test agents
    agents_strict = [
        ("L1 Finance Bear", 1, 'finance', -0.5, 0.8, 0.0, -0.5),
        ("L5 Tech Bull", 5, 'tech', 0.7, -0.7, 0.5, 0.8),
        ("L3 Politics Neutral", 3, 'politics', 0.0, 0.0, 0.0, 0.0),
    ]
    
    points_strict = []
    for name, *params in agents_strict:
        point = strict_manifold.encode_agent_state(*params)
        points_strict.append(point)
        print(f"  {name}:")
        print(f"    Z (hyperbolic): [{point[0]:.3f}, {point[1]:.3f}], radius={np.linalg.norm(point[:2]):.3f}")
        print(f"    Y (circle): [{point[2]:.3f}, {point[3]:.3f}], angle={np.arctan2(point[3], point[2]):.3f}")
        print(f"    X,W,T: [{point[4]:.3f}, {point[5]:.3f}, {point[6]:.3f}]")
        print()
    
    # Distances
    print("  Geodesic Distances (True Riemannian):")
    strict_start = time.time()
    for i in range(len(points_strict)):
        for j in range(i+1, len(points_strict)):
            dist = strict_manifold.cognitive_distance(points_strict[i], points_strict[j])
            print(f"    Dist({agents_strict[i][0]} ↔ {agents_strict[j][0]}): {dist:.4f}")
    strict_dist_time = (time.time() - strict_start) / 3  # Average per pair
    print()
    
    # Metric warping
    shadow_point = strict_manifold.encode_agent_state(4, 'politics', 0.5, -0.9, 0.0, 0.0)
    light_point = strict_manifold.encode_agent_state(1, 'tech', 0.5, 0.9, 0.0, 0.0)
    
    g_shadow = strict_manifold.metric.metric_matrix(shadow_point)
    g_light = strict_manifold.metric.metric_matrix(light_point)
    
    det_shadow = np.linalg.det(g_shadow)
    det_light = np.linalg.det(g_light)
    
    print("  Metric Warping (Shadow Effect):")
    print(f"    det(g) at Shadow (W=-0.9): {det_shadow:.2e}")
    print(f"    det(g) at Light (W=+0.9):  {det_light:.2e}")
    print(f"    Distortion Ratio: {det_shadow/det_light:.2f}x")
    print()
    
    # Coupling test
    interaction_shadow = strict_manifold.metric._interaction_term(shadow_point)
    interaction_light = strict_manifold.metric._interaction_term(light_point)
    
    print("  Z-W Coupling (Hierarchy × Shadow):")
    print(f"    Interaction at Shadow: {interaction_shadow:.4f}")
    print(f"    Interaction at Light:  {interaction_light:.4f}")
    print(f"    Ratio: {interaction_shadow/interaction_light:.2f}x")
    print()
    
    strict_available = True

except Exception as e:
    print(f"❌ Strict implementation error: {e}\n")
    strict_available = False
    strict_init_time = 0
    strict_dist_time = 0

# ============================================================================
# PART 2: Simplified Engineering Implementation
# ============================================================================

print("\n" + "╔" + "═"*78 + "╗")
print("║" + " "*18 + "SIMPLIFIED ENGINEERING IMPLEMENTATION" + " "*23 + "║")
print("╚" + "═"*78 + "╝\n")

try:
    from cpe.raywu_manifold import RaywuCognitiveManifold as SimplifiedManifold
    
    simple_start = time.time()
    simple_manifold = SimplifiedManifold()
    simple_init_time = time.time() - simple_start
    
    print(f"✓ Simplified manifold initialized in {simple_init_time*1000:.2f}ms\n")
    
    # Same test agents
    agents_simple = agents_strict  # Reuse same configs
    
    points_simple = []
    for name, *params in agents_simple:
        point = simple_manifold.encode_agent_state(*params)
        points_simple.append(point)
        print(f"  {name}:")
        print(f"    Z (fake hyperbolic): [{point[0]:.3f}, {point[1]:.3f}], radius={np.linalg.norm(point[:2]):.3f}")
        print(f"    Y (fake sphere): [{point[2]:.3f}, {point[3]:.3f}, {point[4]:.3f}]")
        print(f"    X,W,T,S: [{point[5]:.3f}, {point[6]:.3f}, {point[7]:.3f}, {point[8]:.3f}]")
        print()
    
    # Distances
    print("  Cognitive Distances (Metric-weighted Euclidean):")
    simple_start = time.time()
    for i in range(len(points_simple)):
        for j in range(i+1, len(points_simple)):
            dist = simple_manifold.cognitive_distance(points_simple[i], points_simple[j])
            print(f"    Dist({agents_simple[i][0]} ↔ {agents_simple[j][0]}): {dist:.4f}")
    simple_dist_time = (time.time() - simple_start) / 3
    print()
    
    # Metric warping
    shadow_point_s = simple_manifold.encode_agent_state(4, 'politics', 0.5, -0.9, 0.0, 0.0)
    light_point_s = simple_manifold.encode_agent_state(1, 'tech', 0.5, 0.9, 0.0, 0.0)
    
    g_shadow_s = simple_manifold.metric.metric_matrix(shadow_point_s)
    g_light_s = simple_manifold.metric.metric_matrix(light_point_s)
    
    det_shadow_s = np.linalg.det(g_shadow_s)
    det_light_s = np.linalg.det(g_light_s)
    
    print("  Metric Warping (Shadow Effect):")
    print(f"    det(g) at Shadow (W=-0.9): {det_shadow_s:.2e}")
    print(f"    det(g) at Light (W=+0.9):  {det_light_s:.2e}")
    print(f"    Distortion Ratio: {det_shadow_s/det_light_s:.2e}x")
    print("    ⚠️  This is FAKE distortion (scalar multiplication, not true curvature)")
    print()
    
    simple_available = True

except Exception as e:
    print(f"❌ Simplified implementation error: {e}\n")
    simple_available = False
    simple_init_time = 0
    simple_dist_time = 0

# ============================================================================
# PART 3: Side-by-Side Comparison
# ============================================================================

print("\n" + "╔" + "═"*78 + "╗")
print("║" + " "*26 + "SIDE-BY-SIDE COMPARISON" + " "*29 + "║")
print("╚" + "═"*78 + "╝\n")

if strict_available and simple_available:
    print("┌" + "─"*38 + "┬" + "─"*39 + "┐")
    print("│ {:^36} │ {:^37} │".format("STRICT", "SIMPLIFIED"))
    print("├" + "─"*38 + "┼" + "─"*39 + "┤")
    
    # Manifold structure
    print("│ {:36} │ {:37} │".format("TRUE H²×S¹×R³", "Fake 9D NumPy array"))
    print("│ {:36} │ {:37} │".format("Embedding: 7D", "Embedding: 9D (fake)"))
    print("│ {:36} │ {:37} │".format("Intrinsic: 6D", "Intrinsic: 6D (claimed)"))
    print("├" + "─"*38 + "┼" + "─"*39 + "┤")
    
    # Performance
    print("│ {:36} │ {:37} │".format("Init time:", "Init time:"))
    print("│ {:>36} │ {:>37} │".format(f"{strict_init_time*1000:.2f}ms", f"{simple_init_time*1000:.2f}ms"))
    print("│ {:36} │ {:37} │".format("Distance time:", "Distance time:"))
    print("│ {:>36} │ {:>37} │".format(f"{strict_dist_time*1000:.2f}ms/pair", f"{simple_dist_time*1000:.2f}ms/pair"))
    print("├" + "─"*38 + "┼" + "─"*39 + "┤")
    
    # Shadow distortion
    print("│ {:36} │ {:37} │".format("Shadow distortion:", "Shadow distortion:"))
    print("│ {:>36} │ {:>37} │".format(f"{det_shadow/det_light:.2f}x", f"{det_shadow_s/det_light_s:.2e}x"))
    print("│ {:36} │ {:37} │".format("(TRUE curvature)", "(FAKE scalar mult)"))
    print("├" + "─"*38 + "┼" + "─"*39 + "┤")
    
    # Validation
    print("│ {:36} │ {:37} │".format("Geomstats integration:", "Geomstats integration:"))
    print("│ {:36} │ {:37} │".format("✓ Full (H², S¹, R³)", "✗ Surface-level imports"))
    print("│ {:36} │ {:37} │".format("Geodesic distance:", "Geodesic distance:"))
    print("│ {:36} │ {:37} │".format("✓ True (curved)", "✗ Euclidean (straight)"))
    print("│ {:36} │ {:37} │".format("Metric coupling:", "Metric coupling:"))
    print("│ {:36} │ {:37} │".format("✓ Z-W interaction", "✗ No coupling"))
    print("└" + "─"*38 + "┴" + "─"*39 + "┘")
    
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*32 + "VERDICT" + " "*39 + "║")
    print("╚" + "═"*78 + "╝\n")
    
    print("✓ Strict Implementation:")
    print("  - Mathematically CORRECT (differential geometry)")
    print("  - TRUE geodesic distance (respects curvature)")
    print("  - Proper Z-W coupling (hierarchy × shadow)")
    print(f"  - {det_shadow/det_light:.0f}x shadow distortion (validated)")
    print(f"  - ~{strict_init_time/simple_init_time:.1f}x slower initialization")
    print(f"  - ~{strict_dist_time/simple_dist_time:.1f}x slower distance computation")
    print("  → Use for RESEARCH & VALIDATION")
    print()
    
    print("✓ Simplified Implementation:")
    print("  - Engineering APPROXIMATION (fast but fake)")
    print("  - Metric-weighted Euclidean distance (not geodesic)")
    print("  - No true coupling (scalar warping only)")
    print(f"  - {det_shadow_s/det_light_s:.0e}x fake distortion (misleading)")
    print(f"  - ~{simple_init_time/strict_init_time:.1f}x faster initialization")
    print(f"  - ~{simple_dist_time/strict_dist_time:.1f}x faster distance computation")
    print("  → Use for PROTOTYPES & PRODUCTION")
    print()

else:
    print("⚠️  One or both implementations failed to load.\n")

print("="*80)
print("✅ Comparative demo completed!")
print("="*80)

print("\n📚 For detailed comparison, see: STRICT_VS_SIMPLIFIED.md\n")
