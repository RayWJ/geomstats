"""
Test suite for Cognitive Physics Engine
"""

import pytest
import numpy as np
import torch
import sys
import os

# Add cpe to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cpe'))

from cpe import CognitiveManifold, CognitiveDynamics, Translator, WorldSimulator


class TestCognitiveManifold:
    """Test cases for CognitiveManifold"""
    
    def test_initialization(self):
        """Test manifold initialization"""
        manifold = CognitiveManifold(backend='numpy')
        assert manifold is not None
        assert len(manifold.dim_names) == 6
        
    def test_random_point(self):
        """Test random point generation"""
        manifold = CognitiveManifold(backend='numpy')
        point = manifold.random_point()
        assert len(point) == 6
        
    def test_metric_matrix(self):
        """Test metric tensor computation"""
        manifold = CognitiveManifold(backend='numpy')
        point = np.array([0.1, 0.0, 0.5, 0.0, 0.0, 0.0])
        g = manifold.metric_matrix(point)
        assert g.shape == (6, 6)
        
    def test_distance(self):
        """Test geodesic distance computation"""
        manifold = CognitiveManifold(backend='numpy')
        point_a = np.array([0.1, 0.0, 0.5, 0.0, 0.0, 0.0])
        point_b = np.array([0.8, 0.0, -0.5, 0.0, 0.0, 0.0])
        dist = manifold.distance(point_a, point_b)
        assert dist > 0
        
    def test_interpret_point(self):
        """Test point interpretation"""
        manifold = CognitiveManifold(backend='numpy')
        point = np.array([0.1, 0.0, 0.5, 0.0, 0.0, 0.0])
        interpretation = manifold.interpret_point(point)
        assert 'level' in interpretation
        assert 'stance' in interpretation


class TestCognitiveDynamics:
    """Test cases for CognitiveDynamics"""
    
    def test_initialization(self):
        """Test dynamics initialization"""
        manifold = CognitiveManifold(backend='numpy')
        dynamics = CognitiveDynamics(manifold, hidden_dim=64, n_layers=2)
        assert dynamics is not None
        
    def test_potential_field(self):
        """Test potential field computation"""
        manifold = CognitiveManifold(backend='numpy')
        dynamics = CognitiveDynamics(manifold, hidden_dim=64)
        
        state = torch.randn(10, 6)
        V = dynamics.potential_net(state)
        assert V.shape == (10, 1)
        
    def test_simulate_collapse(self):
        """Test collapse simulation"""
        manifold = CognitiveManifold(backend='numpy')
        dynamics = CognitiveDynamics(manifold, hidden_dim=64, n_layers=2)
        
        initial_points = torch.randn(50, 6) * 0.3
        final_points, _ = dynamics.simulate_collapse(
            initial_points,
            T=2.0,
            dt=0.1,
            method='euler'
        )
        
        assert final_points.shape == initial_points.shape
        # Check that points converged (lower spread)
        assert final_points.std() < initial_points.std()
        
    def test_analyze_equilibrium(self):
        """Test equilibrium analysis"""
        manifold = CognitiveManifold(backend='numpy')
        dynamics = CognitiveDynamics(manifold, hidden_dim=64, n_layers=2)
        
        points = torch.randn(100, 6) * 0.2
        analysis = dynamics.analyze_equilibrium(points, threshold=0.5)
        
        assert 'n_clusters' in analysis
        assert 'clusters' in analysis
        assert analysis['n_clusters'] > 0


class TestTranslator:
    """Test cases for Translator"""
    
    def test_initialization(self):
        """Test translator initialization"""
        manifold = CognitiveManifold(backend='numpy')
        translator = Translator(manifold)
        assert translator is not None
        
    def test_text_to_coordinate(self):
        """Test text to coordinate conversion"""
        manifold = CognitiveManifold(backend='numpy')
        translator = Translator(manifold)
        
        text = "NVIDIA reports strong earnings"
        coord = translator.text_to_coordinate(text)
        
        assert len(coord) == 6
        assert 0 <= coord[0] <= 1  # Z axis (level)
        
    def test_coordinate_to_text(self):
        """Test coordinate to text conversion"""
        manifold = CognitiveManifold(backend='numpy')
        translator = Translator(manifold)
        
        coord = np.array([0.2, 0.3, 0.5, 0.0, 0.0, 0.0])
        text = translator.coordinate_to_text(coord)
        
        assert isinstance(text, str)
        assert len(text) > 0
        
    def test_batch_translate(self):
        """Test batch translation"""
        manifold = CognitiveManifold(backend='numpy')
        translator = Translator(manifold)
        
        texts = [
            "Positive outlook",
            "Negative sentiment",
            "Neutral analysis"
        ]
        
        coords = translator.batch_translate(texts)
        assert coords.shape == (3, 6)
        
    def test_generate_viewpoints(self):
        """Test viewpoint generation"""
        manifold = CognitiveManifold(backend='numpy')
        translator = Translator(manifold)
        
        query = "What is the market outlook?"
        viewpoints = translator.generate_viewpoints(query, n_viewpoints=50)
        
        assert viewpoints.shape == (50, 6)


class TestWorldSimulator:
    """Test cases for WorldSimulator"""
    
    def test_initialization(self):
        """Test simulator initialization"""
        simulator = WorldSimulator(backend='numpy', hidden_dim=64, n_layers=2)
        assert simulator is not None
        assert simulator.manifold is not None
        assert simulator.dynamics is not None
        assert simulator.translator is not None
        
    def test_query(self):
        """Test full query pipeline"""
        simulator = WorldSimulator(backend='numpy', hidden_dim=64, n_layers=2)
        
        result = simulator.query(
            question="What is the outlook for tech stocks?",
            n_viewpoints=50,
            simulation_time=2.0,
            dt=0.1,
            method='euler'
        )
        
        assert 'consensus' in result
        assert 'confidence' in result
        assert 'n_clusters' in result
        assert 0 <= result['confidence'] <= 1
        
    def test_inject_information(self):
        """Test information injection"""
        simulator = WorldSimulator(backend='numpy', hidden_dim=64, n_layers=2)
        
        # Should not raise error
        simulator.inject_information("Breaking news: Major tech partnership")
        
        # Check that barriers were added
        assert len(simulator.dynamics.barriers) > 0


def run_all_tests():
    """Run all tests and print results"""
    print("="*60)
    print("Running Cognitive Physics Engine Test Suite")
    print("="*60 + "\n")
    
    # Run with pytest if available, otherwise manual
    try:
        pytest.main([__file__, '-v'])
    except:
        print("Pytest not available, running manual tests...\n")
        
        test_classes = [
            TestCognitiveManifold(),
            TestCognitiveDynamics(),
            TestTranslator(),
            TestWorldSimulator()
        ]
        
        for test_class in test_classes:
            class_name = test_class.__class__.__name__
            print(f"\n{class_name}:")
            
            test_methods = [m for m in dir(test_class) if m.startswith('test_')]
            
            for method_name in test_methods:
                try:
                    method = getattr(test_class, method_name)
                    method()
                    print(f"  ✓ {method_name}")
                except Exception as e:
                    print(f"  ✗ {method_name}: {str(e)}")


if __name__ == "__main__":
    run_all_tests()
