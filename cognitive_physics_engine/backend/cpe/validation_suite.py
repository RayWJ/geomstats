"""
Raywu Cognitive Physics - Turing Test Suite

This module implements the validation framework to prove the engine
is actually "thinking" in geometric space, not just generating random numbers.

Test Layers:
1. Geometric Structure Validation
2. Dynamical Evolution Validation  
3. Cognitive Turing Test (Hallucination Detection)
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')


class GeometricValidator:
    """
    Test Layer 1: Validate geometric structure correctness.
    
    Tests:
    - Semantic distance consistency
    - Shadow gravity effects
    - Clustering emergence
    """
    
    def __init__(self, manifold):
        self.manifold = manifold
        self.test_results = {}
    
    def test_semantic_distance_consistency(self):
        """
        Test 1: Semantic Distance Consistency
        
        Setup:
        - A: "Company cash flow broken" (Fact, Negative)
        - B: "Company will bankrupt" (Conclusion, Negative)  
        - C: "Company tech leading" (Fact, Positive)
        
        Expected: Dist(A,B) << Dist(A,C)
        
        In Euclidean space (Word2Vec), A and C might be close due to "company".
        In Raywu space, Stance (X-axis) and Logic (Level) differences
        should make A-C distance much larger.
        """
        print("\n" + "="*70)
        print("TEST 1: Semantic Distance Consistency")
        print("="*70)
        
        # Encode test points
        point_A = self.manifold.encode_agent_state(
            level=1,  # Fact
            domain='finance',
            stance=-0.8,  # Negative
            intent=0.8,   # Transparent
            time=0.0,
            scale=0.0
        )
        
        point_B = self.manifold.encode_agent_state(
            level=3,  # Conclusion
            domain='finance',
            stance=-0.9,  # Very negative
            intent=0.7,
            time=0.3,  # Near future
            scale=0.0
        )
        
        point_C = self.manifold.encode_agent_state(
            level=1,  # Fact
            domain='tech',
            stance=0.8,   # Positive
            intent=0.8,
            time=0.0,
            scale=0.0
        )
        
        # Compute distances
        dist_AB = self.manifold.cognitive_distance(point_A, point_B)
        dist_AC = self.manifold.cognitive_distance(point_A, point_C)
        dist_BC = self.manifold.cognitive_distance(point_B, point_C)
        
        print(f"\nPoint A: Cash flow broken (L1, Bearish)")
        print(f"Point B: Will bankrupt (L3, Very bearish)")
        print(f"Point C: Tech leading (L1, Bullish)")
        
        print(f"\nDistances:")
        print(f"  Dist(A ↔ B) = {dist_AB:.4f}  (Similar sentiment)")
        print(f"  Dist(A ↔ C) = {dist_AC:.4f}  (Opposite sentiment)")
        print(f"  Dist(B ↔ C) = {dist_BC:.4f}  (Very opposite)")
        
        # Validation
        ratio_AC_AB = dist_AC / dist_AB
        print(f"\nRatio AC/AB = {ratio_AC_AB:.2f}")
        
        if ratio_AC_AB > 1.5:
            result = "✅ PASS"
            explanation = "Opposite stances create larger distance (geometry works!)"
        else:
            result = "❌ FAIL"
            explanation = "Distance does not respect semantic opposition (flat space?)"
        
        print(f"\n{result}: {explanation}")
        
        self.test_results['semantic_consistency'] = {
            'passed': ratio_AC_AB > 1.5,
            'ratio': ratio_AC_AB,
            'distances': {'AB': dist_AB, 'AC': dist_AC, 'BC': dist_BC}
        }
        
        return self.test_results['semantic_consistency']
    
    def test_shadow_gravity_effect(self):
        """
        Test 2: Shadow Dimension Gravity Effect
        
        Setup: Perfect Ponzi scheme case
        - Surface logic (L5/L3): Perfect loop, high growth
        - Hidden intent (W): Founder cashing out
        
        Operation: Gradually increase W-axis weight (shadow score)
        
        Expected: Geodesics should bend dramatically when shadow increases,
        like light bending near a black hole.
        """
        print("\n" + "="*70)
        print("TEST 2: Shadow Gravity Effect")
        print("="*70)
        
        print("\nSetup: Analyzing a 'perfect' Ponzi scheme")
        print("  Surface: High growth, closed loop logic")
        print("  Reality: Hidden cashing-out intent")
        
        # Test points with varying shadow levels
        shadow_levels = [-0.9, -0.6, -0.3, 0.0, 0.3]
        metric_dets = []
        
        for w in shadow_levels:
            point = self.manifold.encode_agent_state(
                level=5,  # Speculation level
                domain='finance',
                stance=0.7,  # Looks bullish
                intent=w,    # Varying shadow
                time=0.5,
                scale=0.5
            )
            
            g = self.manifold.metric.metric_matrix(point)
            det_g = np.linalg.det(g)
            metric_dets.append(det_g)
            
            print(f"\nW={w:+.1f} (Shadow level)")
            print(f"  Metric determinant: {det_g:.2e}")
        
        # Analysis
        print(f"\n{'Shadow Level':<15} {'Metric Det':<15} {'Relative'}")
        print("-" * 50)
        baseline = metric_dets[3]  # W=0.0
        
        for i, w in enumerate(shadow_levels):
            ratio = metric_dets[i] / baseline
            print(f"W={w:+.1f}           {metric_dets[i]:.2e}      {ratio:>8.1f}x")
        
        # Validation
        max_ratio = max(metric_dets) / baseline
        
        if max_ratio > 10.0:
            result = "✅ PASS"
            explanation = f"Shadow creates {max_ratio:.0f}x volume distortion (gravity works!)"
        else:
            result = "❌ FAIL"
            explanation = "Shadow does not create sufficient metric warping"
        
        print(f"\n{result}: {explanation}")
        
        self.test_results['shadow_gravity'] = {
            'passed': max_ratio > 10.0,
            'max_ratio': max_ratio,
            'metric_dets': metric_dets
        }
        
        return self.test_results['shadow_gravity']
    
    def test_clustering_emergence(self):
        """
        Test 3: Natural Clustering in Manifold
        
        Generate random agents and check if natural clusters emerge
        based on Level, Stance, and Intent.
        """
        print("\n" + "="*70)
        print("TEST 3: Clustering Emergence")
        print("="*70)
        
        print("\nGenerating 50 random agents...")
        
        # Generate agents in different "camps"
        agents = []
        
        # Camp 1: L1 Bears (Pessimistic facts)
        for _ in range(15):
            agents.append(self.manifold.encode_agent_state(
                level=np.random.randint(1, 3),
                domain='finance',
                stance=np.random.uniform(-1.0, -0.4),
                intent=np.random.uniform(0.5, 1.0),
                time=0.0,
                scale=0.0
            ))
        
        # Camp 2: L5 Bulls (Optimistic speculation)
        for _ in range(15):
            agents.append(self.manifold.encode_agent_state(
                level=np.random.randint(4, 6),
                domain='tech',
                stance=np.random.uniform(0.4, 1.0),
                intent=np.random.uniform(0.3, 0.9),
                time=0.5,
                scale=0.5
            ))
        
        # Camp 3: Shadow operators (Hidden agenda)
        for _ in range(10):
            agents.append(self.manifold.encode_agent_state(
                level=np.random.randint(3, 5),
                domain='politics',
                stance=np.random.uniform(-0.3, 0.3),
                intent=np.random.uniform(-1.0, -0.4),
                time=0.0,
                scale=0.0
            ))
        
        # Camp 4: Neutrals
        for _ in range(10):
            agents.append(self.manifold.encode_agent_state(
                level=3,
                domain='finance',
                stance=np.random.uniform(-0.2, 0.2),
                intent=np.random.uniform(0.0, 0.5),
                time=0.0,
                scale=0.0
            ))
        
        agents = np.array(agents)
        
        # Compute distance matrix
        print("\nComputing pairwise distances...")
        n = len(agents)
        dist_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i+1, n):
                dist = self.manifold.cognitive_distance(agents[i], agents[j])
                dist_matrix[i, j] = dist
                dist_matrix[j, i] = dist
        
        # Simple clustering: Intra-camp vs Inter-camp distances
        camp_boundaries = [0, 15, 30, 40, 50]
        
        intra_distances = []
        inter_distances = []
        
        for c in range(4):
            start, end = camp_boundaries[c], camp_boundaries[c+1]
            # Intra-camp
            for i in range(start, end):
                for j in range(i+1, end):
                    intra_distances.append(dist_matrix[i, j])
            # Inter-camp
            for i in range(start, end):
                for j in range(end, n):
                    inter_distances.append(dist_matrix[i, j])
        
        avg_intra = np.mean(intra_distances)
        avg_inter = np.mean(inter_distances)
        separation_ratio = avg_inter / avg_intra
        
        print(f"\nClustering Analysis:")
        print(f"  Average intra-camp distance: {avg_intra:.4f}")
        print(f"  Average inter-camp distance: {avg_inter:.4f}")
        print(f"  Separation ratio: {separation_ratio:.2f}")
        
        if separation_ratio > 1.3:
            result = "✅ PASS"
            explanation = f"Natural clusters emerge ({separation_ratio:.1f}x separation)"
        else:
            result = "❌ FAIL"
            explanation = "No clear clustering (agents too uniformly distributed)"
        
        print(f"\n{result}: {explanation}")
        
        self.test_results['clustering'] = {
            'passed': separation_ratio > 1.3,
            'separation_ratio': separation_ratio,
            'avg_intra': avg_intra,
            'avg_inter': avg_inter
        }
        
        return self.test_results['clustering']
    
    def run_all_tests(self):
        """Run all geometric validation tests."""
        print("\n" + "🔬"*35)
        print("GEOMETRIC STRUCTURE VALIDATION SUITE")
        print("🔬"*35)
        
        self.test_semantic_distance_consistency()
        self.test_shadow_gravity_effect()
        self.test_clustering_emergence()
        
        # Summary
        print("\n" + "="*70)
        print("VALIDATION SUMMARY")
        print("="*70)
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results.values() if r['passed'])
        
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"{test_name:<30}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All geometric tests passed!")
            print("The manifold structure correctly captures cognitive distances.")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed.")
            print("The geometric structure may need adjustment.")
        
        return self.test_results


if __name__ == "__main__":
    from raywu_manifold import RaywuCognitiveManifold
    
    print("\n" + "🧪"*35)
    print("RAYWU COGNITIVE PHYSICS - TURING TEST")
    print("🧪"*35)
    
    manifold = RaywuCognitiveManifold()
    validator = GeometricValidator(manifold)
    
    results = validator.run_all_tests()
