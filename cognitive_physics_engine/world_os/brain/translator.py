"""
Neuro-Symbolic Translator - Bridge Between Text and Tensor
===========================================================

This module connects the symbolic world (Markdown text) with the 
subsymbolic world (manifold tensors).

Philosophy:
- Text is how humans think
- Tensors are how physics computes
- Translation is the key to hybrid intelligence

Functions:
1. text_to_tensor: Parse Markdown → Extract state coordinates
2. tensor_to_text: Analyze trajectory → Generate narrative
3. text_to_potential: Parse constraints → Build potential field V(x)

Author: Raywu WorldOS Team  
Date: 2026-02-01
Version: v61.0
"""

import re
import json
import numpy as np
from typing import Dict, Any, Optional
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "kernel"))

from manifold import CognitiveManifold
from dynamics import PotentialField


class NeuroSymbolicTranslator:
    """
    The Bridge between Language and Geometry
    
    This class performs bidirectional translation:
    - Markdown → Manifold coordinates
    - Trajectory → Narrative description
    """
    
    def __init__(self, manifold: CognitiveManifold):
        """
        Initialize translator with a manifold instance.
        
        Args:
            manifold: CognitiveManifold for encoding/decoding
        """
        self.manifold = manifold
    
    def parse_frontmatter(self, markdown: str) -> Dict[str, Any]:
        """
        Extract YAML frontmatter from Markdown.
        
        Format:
        ---
        level: L3
        domain: tech
        stance: 0.7
        ---
        """
        metadata = {}
        
        if markdown.startswith("---"):
            parts = markdown.split("---", 2)
            if len(parts) >= 3:
                yaml_text = parts[1]
                for line in yaml_text.strip().split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Try to parse as number
                        try:
                            if "." in value:
                                value = float(value)
                            else:
                                value = int(value)
                        except ValueError:
                            pass  # Keep as string
                        
                        metadata[key] = value
        
        return metadata
    
    def text_to_tensor(self, markdown: str) -> np.ndarray:
        """
        Convert Markdown document to manifold coordinates.
        
        Process:
        1. Parse frontmatter (level, domain, stance, etc.)
        2. Encode using manifold.encode_state()
        3. Return coordinates
        
        Args:
            markdown: Markdown document content
        
        Returns:
            10D numpy array (position on manifold)
        """
        # Parse metadata
        metadata = self.parse_frontmatter(markdown)
        
        # Extract semantic attributes (with defaults)
        level_str = str(metadata.get("level", "L3"))
        if level_str.startswith("L"):
            level = int(level_str[1])
        else:
            level = 3
        
        domain = metadata.get("domain", "tech")
        stance = float(metadata.get("stance", 0.0))
        intent = float(metadata.get("intent", 0.0))
        time = float(metadata.get("time", 0.0))
        scale = float(metadata.get("scale", 0.0))
        
        # Encode to manifold
        point = self.manifold.encode_state(level, domain, stance, intent, time, scale)
        
        return point
    
    def tensor_to_text(self, point: np.ndarray, trajectory: Optional[np.ndarray] = None) -> str:
        """
        Convert manifold coordinates (and trajectory) to narrative text.
        
        Args:
            point: Final position on manifold
            trajectory: Optional full trajectory (for analysis)
        
        Returns:
            Markdown-formatted narrative
        """
        # Decode coordinates
        decoded = self.manifold.decode_state(point)
        
        # Build narrative
        lines = []
        lines.append(f"# State Update")
        lines.append(f"")
        lines.append(f"**Level**: {decoded['level']}")
        lines.append(f"**Domain**: {decoded['domain']}")
        lines.append(f"**Stance**: {decoded['stance']}")
        lines.append(f"**Intent**: {decoded['intent']}")
        lines.append(f"**Time Focus**: {decoded['time_focus']}")
        lines.append(f"**Scale**: {decoded['scale']}")
        lines.append(f"")
        
        # If trajectory provided, analyze it
        if trajectory is not None and len(trajectory) > 1:
            lines.append(f"## Physics Analysis")
            lines.append(f"")
            
            # Compute drift
            drift = np.linalg.norm(trajectory[-1] - trajectory[0])
            lines.append(f"**Drift**: {drift:.4f} (total displacement)")
            
            # Trend
            if drift > 1.0:
                lines.append(f"**Trend**: Significant movement observed")
            else:
                lines.append(f"**Trend**: Relatively stable")
            
            lines.append(f"")
        
        lines.append(f"## Raw Coordinates")
        lines.append(f"```json")
        lines.append(json.dumps(decoded['coordinates'], indent=2))
        lines.append(f"```")
        
        return "\n".join(lines)
    
    def text_to_potential(self, markdown: str) -> PotentialField:
        """
        Extract constraints from text and build potential field.
        
        This is a simplified version. Full implementation would use LLM
        to understand natural language constraints.
        
        Args:
            markdown: Document describing goals/constraints
        
        Returns:
            PotentialField instance
        """
        potential = PotentialField()
        
        # Simple keyword-based extraction
        # In practice, this would use GPT-4 to understand intent
        
        # Look for "goal:" patterns
        goal_matches = re.findall(r'goal:\s*(.+)', markdown, re.IGNORECASE)
        for match in goal_matches:
            # Parse goal (simplified: assume bullish/bearish keywords)
            if 'bull' in match.lower():
                target = self.manifold.encode_state(2, 'tech', 0.7, 0.8, 0.3, 0.0)
                potential.add_attractor(target, strength=0.5, radius=1.0)
            elif 'bear' in match.lower():
                target = self.manifold.encode_state(2, 'tech', -0.7, 0.8, 0.3, 0.0)
                potential.add_attractor(target, strength=0.5, radius=1.0)
        
        # Look for "avoid:" patterns
        avoid_matches = re.findall(r'avoid:\s*(.+)', markdown, re.IGNORECASE)
        for match in avoid_matches:
            if 'bankruptcy' in match.lower() or 'risk' in match.lower():
                danger = self.manifold.encode_state(1, 'finance', -0.9, -0.9, -0.5, -0.8)
                potential.add_barrier(danger, strength=1.0, radius=0.8)
        
        return potential


# ============================================================================
# DEMO
# ============================================================================

def demo_translator():
    """Demonstrate text ↔ tensor translation."""
    print("\n" + "="*70)
    print("🌉 NEURO-SYMBOLIC TRANSLATOR DEMO")
    print("="*70 + "\n")
    
    # Create manifold
    manifold = CognitiveManifold()
    translator = NeuroSymbolicTranslator(manifold)
    
    # Sample Markdown
    sample_md = """---
level: L2
domain: tech
stance: 0.6
intent: 0.8
time: 0.3
scale: 0.2
---

# Entity: TechCorp

## Current State
Bullish momentum with strong fundamentals.

## Goals
Goal: Maintain bullish trend while managing risks.

## Constraints
Avoid: Overvaluation risk and market correction.
"""
    
    print("Sample Markdown:")
    print("-" * 40)
    print(sample_md)
    print("-" * 40 + "\n")
    
    # Text → Tensor
    print("🔽 TEXT → TENSOR")
    point = translator.text_to_tensor(sample_md)
    print(f"  Encoded coordinates: {point}")
    print()
    
    # Tensor → Text
    print("🔼 TENSOR → TEXT")
    narrative = translator.tensor_to_text(point)
    print(narrative)
    print()
    
    # Text → Potential
    print("⚡ TEXT → POTENTIAL FIELD")
    potential = translator.text_to_potential(sample_md)
    print(f"  Attractors: {len(potential.wells)}")
    print(f"  Barriers: {len(potential.barriers)}")
    
    print("\n" + "="*70)
    print("✅ Translator demo completed!")
    print("="*70)


if __name__ == "__main__":
    demo_translator()
