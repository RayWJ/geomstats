"""
Translator: Bridge between natural language and geometric coordinates

This module converts between:
- Text (LLM output) ↔ 6D Manifold Coordinates
- Semantic concepts ↔ Geometric positions
- Natural language ↔ Mathematical representation

Uses LLM for semantic understanding and embedding models for encoding.
"""

import numpy as np
import torch
from typing import Dict, List, Optional, Any
import json
import re


class MockLLM:
    """
    Mock LLM client for testing.
    Replace with actual LLM API (OpenAI, Anthropic, etc.) in production.
    """
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Parse text into semantic components.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with semantic attributes
        """
        # Simple rule-based analysis for demo
        result = {
            'level': 3,  # Default to L3
            'domain': 'general',
            'stance': 0.0,  # Neutral
            'intent': 0.0,  # Neutral
            'time': 0.0,  # Present
            'scale': 0.0   # Medium
        }
        
        text_lower = text.lower()
        
        # Level detection
        if any(word in text_lower for word in ['fact', 'data', 'report', 'confirmed']):
            result['level'] = 1
        elif any(word in text_lower for word in ['analysis', 'study', 'research']):
            result['level'] = 2
        elif any(word in text_lower for word in ['strategy', 'recommend', 'suggest']):
            result['level'] = 3
        elif any(word in text_lower for word in ['opinion', 'think', 'believe']):
            result['level'] = 4
        elif any(word in text_lower for word in ['speculation', 'maybe', 'could', 'might']):
            result['level'] = 5
        
        # Domain detection
        if any(word in text_lower for word in ['nvidia', 'chip', 'gpu', 'ai', 'tech']):
            result['domain'] = 'tech'
        elif any(word in text_lower for word in ['finance', 'stock', 'market', 'trading']):
            result['domain'] = 'finance'
        elif any(word in text_lower for word in ['politics', 'government', 'policy']):
            result['domain'] = 'politics'
        
        # Stance detection
        bullish_words = ['bullish', 'positive', 'growth', 'rise', 'buy', 'optimistic', 'strong']
        bearish_words = ['bearish', 'negative', 'decline', 'fall', 'sell', 'pessimistic', 'weak']
        
        bull_count = sum(1 for word in bullish_words if word in text_lower)
        bear_count = sum(1 for word in bearish_words if word in text_lower)
        
        if bull_count > bear_count:
            result['stance'] = 0.7
        elif bear_count > bull_count:
            result['stance'] = -0.7
        
        # Intent detection
        positive_intent = ['constructive', 'helpful', 'transparent', 'honest']
        negative_intent = ['manipulation', 'deception', 'hidden', 'agenda']
        
        if any(word in text_lower for word in negative_intent):
            result['intent'] = -0.5
        elif any(word in text_lower for word in positive_intent):
            result['intent'] = 0.5
        
        # Time detection
        if any(word in text_lower for word in ['future', 'will', 'forecast', 'predict']):
            result['time'] = 0.5
        elif any(word in text_lower for word in ['past', 'was', 'historical', 'previous']):
            result['time'] = -0.5
        
        # Scale detection
        if any(word in text_lower for word in ['macro', 'global', 'industry', 'market-wide']):
            result['scale'] = 0.7
        elif any(word in text_lower for word in ['micro', 'individual', 'specific', 'detail']):
            result['scale'] = -0.7
        
        return result


class Translator:
    """
    Translates between natural language and manifold coordinates.
    
    Core functionality:
    1. text_to_coordinate: Text → 6D point
    2. coordinate_to_text: 6D point → Text description
    3. batch_translate: Multiple texts → Multiple points
    4. update_potential_field: New information → Modify dynamics
    """
    
    def __init__(self, manifold, dynamics=None, llm=None):
        """
        Initialize translator.
        
        Args:
            manifold: CognitiveManifold instance
            dynamics: CognitiveDynamics instance (optional)
            llm: LLM client instance (optional, uses mock if None)
        """
        self.manifold = manifold
        self.dynamics = dynamics
        self.llm = llm if llm is not None else MockLLM()
        
        # Domain encoding (simple mapping)
        self.domain_map = {
            'general': 0.0,
            'tech': 0.3,
            'finance': -0.3,
            'politics': 0.6,
            'science': -0.6
        }
    
    def text_to_coordinate(self, text: str) -> np.ndarray:
        """
        Convert text to 6D manifold coordinate.
        
        Pipeline:
        1. LLM analyzes semantic content
        2. Map semantic attributes to dimensions
        3. Return 6D coordinate [z, y, x, w, t, s]
        
        Args:
            text: Input text
            
        Returns:
            6D numpy array representing position on manifold
        """
        # Step 1: Semantic analysis
        semantic = self.llm.analyze(text)
        
        # Step 2: Map to coordinates
        coord = self._semantic_to_coordinate(semantic)
        
        return coord
    
    def _semantic_to_coordinate(self, semantic: Dict[str, Any]) -> np.ndarray:
        """
        Map semantic dictionary to 6D coordinate.
        
        Args:
            semantic: Dictionary with keys (level, domain, stance, intent, time, scale)
            
        Returns:
            6D coordinate
        """
        # Z: Level (1-5 → 0.0-1.0)
        z = (semantic['level'] - 1) / 4.0
        
        # Y: Domain (mapped to range)
        domain_key = semantic.get('domain', 'general')
        y = self.domain_map.get(domain_key, 0.0)
        
        # X: Stance (-1 to 1)
        x = np.clip(semantic['stance'], -1.0, 1.0)
        
        # W: Intent (-1 to 1)
        w = np.clip(semantic['intent'], -1.0, 1.0)
        
        # T: Time (-1 to 1)
        t = np.clip(semantic['time'], -1.0, 1.0)
        
        # S: Scale (-1 to 1)
        s = np.clip(semantic['scale'], -1.0, 1.0)
        
        return np.array([z, y, x, w, t, s], dtype=np.float32)
    
    def coordinate_to_text(self, coord: np.ndarray) -> str:
        """
        Convert 6D coordinate back to text description.
        
        Args:
            coord: 6D coordinate [z, y, x, w, t, s]
            
        Returns:
            Human-readable description
        """
        interpretation = self.manifold.interpret_point(coord)
        
        # Build description
        parts = []
        
        # Level
        parts.append(f"Level: {interpretation['level']}")
        
        # Domain
        domain = 'Tech' if interpretation['domain_coord'] > 0.2 else \
                 'Finance' if interpretation['domain_coord'] < -0.2 else 'General'
        parts.append(f"Domain: {domain}")
        
        # Stance
        parts.append(f"Stance: {interpretation['stance']}")
        
        # Intent
        parts.append(f"Intent: {interpretation['intent']}")
        
        # Time
        time_desc = 'Future-oriented' if interpretation['time'] > 0.3 else \
                   'Past-focused' if interpretation['time'] < -0.3 else 'Present'
        parts.append(f"Time: {time_desc}")
        
        # Scale
        scale_desc = 'Macro' if interpretation['scale'] > 0.3 else \
                    'Micro' if interpretation['scale'] < -0.3 else 'Medium'
        parts.append(f"Scale: {scale_desc}")
        
        return " | ".join(parts)
    
    def batch_translate(self, texts: List[str]) -> np.ndarray:
        """
        Translate multiple texts to coordinates.
        
        Args:
            texts: List of text strings
            
        Returns:
            (N, 6) numpy array of coordinates
        """
        coords = []
        for text in texts:
            coord = self.text_to_coordinate(text)
            coords.append(coord)
        
        return np.array(coords)
    
    def generate_viewpoints(
        self,
        query: str,
        n_viewpoints: int = 100,
        diversity: float = 0.3
    ) -> torch.Tensor:
        """
        Generate diverse viewpoints around a query.
        
        This creates the initial population for simulation.
        
        Args:
            query: Central query/topic
            n_viewpoints: Number of viewpoints to generate
            diversity: Standard deviation of noise (higher = more diverse)
            
        Returns:
            (n_viewpoints, 6) tensor of initial positions
        """
        # Get center coordinate from query
        center_coord = self.text_to_coordinate(query)
        center_tensor = torch.from_numpy(center_coord).float()
        
        # Generate variations with Gaussian noise
        noise = torch.randn(n_viewpoints, 6) * diversity
        viewpoints = center_tensor.unsqueeze(0) + noise
        
        # Clip to valid ranges
        viewpoints[:, 0] = torch.clamp(viewpoints[:, 0], 0.0, 1.0)  # Z: 0-1
        viewpoints[:, 2:] = torch.clamp(viewpoints[:, 2:], -1.0, 1.0)  # X,W,T,S: -1 to 1
        
        return viewpoints
    
    def update_potential_field(self, new_info: str):
        """
        Update potential field based on new information.
        
        When breaking news arrives, this modifies the dynamics
        by adding repulsive/attractive forces.
        
        Args:
            new_info: New information text (e.g., "NVIDIA earnings miss")
        """
        if self.dynamics is None:
            raise ValueError("Dynamics not initialized. Cannot update potential field.")
        
        # Parse new information
        coord = self.text_to_coordinate(new_info)
        coord_tensor = torch.from_numpy(coord).float()
        
        # Determine impact type
        semantic = self.llm.analyze(new_info)
        
        # Negative news → Repulsive barrier (push away)
        # Positive news → Attractive well (pull towards)
        if semantic['stance'] < -0.3:
            # Bearish news: Create repulsive barrier
            self.dynamics.add_potential_barrier(
                center=coord_tensor,
                height=50.0,  # Strong repulsion
                width=0.3
            )
        elif semantic['stance'] > 0.3:
            # Bullish news: Create attractive well (negative barrier)
            self.dynamics.add_potential_barrier(
                center=coord_tensor,
                height=-30.0,  # Attraction
                width=0.3
            )
        
        print(f"✓ Potential field updated with: {new_info[:50]}...")
    
    def synthesize_consensus(
        self,
        final_points: torch.Tensor,
        method: str = 'centroid'
    ) -> str:
        """
        Synthesize final consensus from equilibrium points.
        
        Args:
            final_points: (N, 6) tensor of final positions
            method: 'centroid' or 'weighted_average'
            
        Returns:
            Natural language consensus statement
        """
        if method == 'centroid':
            # Simple centroid
            consensus_coord = final_points.mean(dim=0).cpu().numpy()
        else:
            # Could weight by density, potential energy, etc.
            consensus_coord = final_points.mean(dim=0).cpu().numpy()
        
        # Convert back to text
        interpretation = self.manifold.interpret_point(consensus_coord)
        
        # Build consensus statement
        level = interpretation['level']
        stance = interpretation['stance']
        intent = interpretation['intent']
        
        if 'L1' in level:
            certainty = "Based on verified facts"
        elif 'L2' in level:
            certainty = "Based on data analysis"
        elif 'L3' in level:
            certainty = "Strategic assessment suggests"
        elif 'L4' in level:
            certainty = "Prevailing opinion is"
        else:
            certainty = "Speculation indicates"
        
        if stance == "Bullish":
            recommendation = "positive outlook"
        elif stance == "Bearish":
            recommendation = "negative outlook"
        else:
            recommendation = "neutral stance"
        
        if intent == "Constructive":
            tone = "with high confidence"
        else:
            tone = "with caution"
        
        consensus = f"{certainty}, the consensus is a {recommendation} {tone}."
        
        return consensus


if __name__ == "__main__":
    print("=== Translator Test ===")
    
    # Import dependencies
    import sys
    sys.path.append('..')
    from manifold import CognitiveManifold
    from dynamics import CognitiveDynamics
    
    manifold = CognitiveManifold(backend='numpy')
    dynamics = CognitiveDynamics(manifold)
    translator = Translator(manifold, dynamics)
    
    # Test text → coordinate
    test_texts = [
        "NVIDIA reports strong Q4 earnings with revenue growth",
        "Analysts believe the chip sector may face headwinds",
        "Historical data shows tech stocks are volatile",
        "My personal opinion is bullish on AI infrastructure"
    ]
    
    print("\n--- Text to Coordinate ---")
    for text in test_texts:
        coord = translator.text_to_coordinate(text)
        desc = translator.coordinate_to_text(coord)
        print(f"\nText: {text[:60]}")
        print(f"Coord: {coord}")
        print(f"Interpretation: {desc}")
    
    # Test viewpoint generation
    print("\n--- Generate Viewpoints ---")
    query = "What is the outlook for NVIDIA?"
    viewpoints = translator.generate_viewpoints(query, n_viewpoints=50)
    print(f"Generated {viewpoints.shape[0]} viewpoints")
    print(f"Viewpoint spread: {viewpoints.std(dim=0).mean():.4f}")
    
    # Test potential field update
    print("\n--- Update Potential Field ---")
    news = "NVIDIA announces major production delays"
    translator.update_potential_field(news)
    
    print("\n✓ Translator test completed!")
