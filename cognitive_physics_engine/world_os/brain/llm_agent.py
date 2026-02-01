"""
LLM Agent - Real AI-Powered Decision Making
============================================

This module integrates real LLM (GPT-4, Claude, etc.) for cognitive decision-making
in the WorldOS tick system.

Features:
1. Trajectory analysis (understand what happened)
2. Strategic intervention (decide when/how to act)
3. Constraint extraction (natural language → potential fields)
4. Narrative generation (explain dynamics in human terms)

Author: Raywu WorldOS Team
Date: 2026-02-01
Version: v61.0
"""

import os
import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI library not available. Install with: pip install openai")


class LLMAgent:
    """
    AI-powered cognitive agent using real LLM.
    
    This class wraps LLM APIs to provide intelligent decision-making
    for WorldOS simulation interventions.
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 model: str = "gpt-4",
                 base_url: Optional[str] = None):
        """
        Initialize LLM agent.
        
        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            model: Model name (gpt-4, gpt-3.5-turbo, etc.)
            base_url: Custom base URL for OpenAI-compatible APIs
        """
        self.model = model
        
        if OPENAI_AVAILABLE:
            # Initialize OpenAI client
            self.client = OpenAI(
                api_key=api_key or os.getenv("OPENAI_API_KEY"),
                base_url=base_url
            )
            self.available = True
            print(f"✓ LLM Agent initialized (model: {model})")
        else:
            self.client = None
            self.available = False
            print("⚠️  LLM Agent unavailable (OpenAI library not installed)")
    
    def analyze_trajectory(self, 
                          initial_state: Dict[str, Any],
                          final_state: Dict[str, Any],
                          trajectory_stats: Dict[str, float],
                          entity_context: str = "") -> Dict[str, Any]:
        """
        Analyze trajectory and provide insights.
        
        Args:
            initial_state: Decoded initial state
            final_state: Decoded final state
            trajectory_stats: Physics statistics (distance, drift, volatility)
            entity_context: Additional context about the entity
        
        Returns:
            Dictionary with analysis results
        """
        if not self.available:
            return self._fallback_analysis(initial_state, final_state, trajectory_stats)
        
        # Build prompt
        prompt = self._build_analysis_prompt(
            initial_state, final_state, trajectory_stats, entity_context
        )
        
        try:
            # Call LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse response
            analysis_text = response.choices[0].message.content
            
            return {
                "status": "success",
                "analysis": analysis_text,
                "model": self.model,
                "tokens_used": response.usage.total_tokens
            }
        
        except Exception as e:
            print(f"⚠️  LLM call failed: {e}")
            return self._fallback_analysis(initial_state, final_state, trajectory_stats)
    
    def decide_intervention(self,
                           analysis: Dict[str, Any],
                           risk_threshold: float = 0.7) -> Dict[str, Any]:
        """
        Decide whether to intervene and how.
        
        Args:
            analysis: Output from analyze_trajectory()
            risk_threshold: Threshold for triggering intervention
        
        Returns:
            Dictionary with intervention decision
        """
        if not self.available:
            return self._fallback_intervention(analysis)
        
        # Build prompt for intervention decision
        prompt = f"""Based on this trajectory analysis:

{analysis.get('analysis', 'No analysis available')}

Should we intervene? Consider:
1. Is there significant risk or opportunity?
2. Would intervention improve outcomes?
3. What specific actions should be taken?

Respond in JSON format:
{{
    "should_intervene": true/false,
    "confidence": 0.0-1.0,
    "reasoning": "explanation",
    "recommended_actions": ["action1", "action2"]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for decision-making
                max_tokens=300,
                response_format={"type": "json_object"}
            )
            
            decision = json.loads(response.choices[0].message.content)
            decision["status"] = "success"
            decision["model"] = self.model
            
            return decision
        
        except Exception as e:
            print(f"⚠️  LLM intervention decision failed: {e}")
            return self._fallback_intervention(analysis)
    
    def extract_potential_field(self, 
                               natural_language: str) -> Dict[str, Any]:
        """
        Extract attractors/barriers from natural language description.
        
        Args:
            natural_language: Text describing goals, constraints, risks
        
        Returns:
            Dictionary with potential field specifications
        """
        if not self.available:
            return self._fallback_potential_extraction(natural_language)
        
        prompt = f"""Extract goal attractors and risk barriers from this description:

{natural_language}

For each attractor/barrier, specify:
- type: "attractor" or "barrier"
- description: what it represents
- strength: 0.0-1.0 (how strong the pull/push)
- target: semantic coordinates (level, domain, stance, intent)

Respond in JSON format:
{{
    "attractors": [
        {{"description": "...", "strength": 0.5, "target": {{"level": "L3", "domain": "tech", "stance": 0.7, "intent": 0.5}}}}
    ],
    "barriers": [
        {{"description": "...", "strength": 0.8, "target": {{"level": "L1", "domain": "finance", "stance": -0.9, "intent": -0.9}}}}
    ]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            field_spec = json.loads(response.choices[0].message.content)
            field_spec["status"] = "success"
            field_spec["model"] = self.model
            
            return field_spec
        
        except Exception as e:
            print(f"⚠️  LLM potential field extraction failed: {e}")
            return self._fallback_potential_extraction(natural_language)
    
    def generate_narrative(self,
                          trajectory_analysis: Dict[str, Any],
                          entity_name: str) -> str:
        """
        Generate human-readable narrative from trajectory.
        
        Args:
            trajectory_analysis: Output from analyze_trajectory()
            entity_name: Name of the entity (e.g., "NVIDIA")
        
        Returns:
            Narrative text
        """
        if not self.available:
            return self._fallback_narrative(trajectory_analysis, entity_name)
        
        prompt = f"""Generate a concise narrative explaining what happened to {entity_name}:

Analysis:
{trajectory_analysis.get('analysis', 'No analysis')}

Write 2-3 sentences suitable for a financial report or strategy memo.
Focus on the key dynamics and implications.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a financial analyst writing clear, actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"⚠️  LLM narrative generation failed: {e}")
            return self._fallback_narrative(trajectory_analysis, entity_name)
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for LLM."""
        return """You are an expert cognitive physics analyst working with the WorldOS simulation.

Your role is to:
1. Analyze trajectories on a 6D cognitive manifold (Z-Level, Y-Domain, X-Stance, W-Intent, T-Time, S-Scale)
2. Understand the physics: entities move under Langevin dynamics with friction and potential fields
3. Identify risks, opportunities, and strategic interventions
4. Provide actionable insights for decision-making

Key concepts:
- Z (Level): L5 (strategy) → L3 (logic) → L1 (facts)
- Y (Domain): tech, finance, politics, etc.
- X (Stance): bullish (+) to bearish (-)
- W (Intent): constructive (+) to shadow/hidden (-)
- Cognitive distance: Riemannian distance on curved manifold
- Shadow regions: High friction, low visibility (W < -0.3)

Be concise, quantitative, and strategic."""
    
    def _build_analysis_prompt(self,
                               initial_state: Dict[str, Any],
                               final_state: Dict[str, Any],
                               trajectory_stats: Dict[str, float],
                               context: str) -> str:
        """Build analysis prompt."""
        return f"""Analyze this cognitive trajectory:

INITIAL STATE:
- Level: {initial_state.get('level', 'N/A')}
- Domain: {initial_state.get('domain', 'N/A')}
- Stance: {initial_state.get('stance', 'N/A')}
- Intent: {initial_state.get('intent', 'N/A')}

FINAL STATE:
- Level: {final_state.get('level', 'N/A')}
- Domain: {final_state.get('domain', 'N/A')}
- Stance: {final_state.get('stance', 'N/A')}
- Intent: {final_state.get('intent', 'N/A')}

PHYSICS METRICS:
- Cognitive distance traveled: {trajectory_stats.get('distance', 0):.4f}
- Drift: {trajectory_stats.get('drift', 0):.4f}
- Volatility: {trajectory_stats.get('volatility', 0):.4f}

CONTEXT:
{context or 'No additional context'}

What happened? What are the key dynamics? Any risks or opportunities?"""
    
    def _fallback_analysis(self, initial_state, final_state, stats) -> Dict[str, Any]:
        """Fallback analysis when LLM unavailable."""
        level_change = initial_state.get('level', '') != final_state.get('level', '')
        stance_initial = initial_state.get('stance', '')
        stance_final = final_state.get('stance', '')
        distance = stats.get('distance', 0)
        
        analysis_parts = []
        
        if level_change:
            analysis_parts.append(f"Level shifted from {initial_state.get('level')} to {final_state.get('level')}.")
        
        if stance_initial != stance_final:
            analysis_parts.append(f"Stance changed from {stance_initial} to {stance_final}.")
        
        if distance > 1.0:
            analysis_parts.append(f"Significant movement detected (distance: {distance:.2f}).")
        else:
            analysis_parts.append("Trajectory remained relatively stable.")
        
        return {
            "status": "fallback",
            "analysis": " ".join(analysis_parts),
            "model": "rule-based"
        }
    
    def _fallback_intervention(self, analysis) -> Dict[str, Any]:
        """Fallback intervention decision."""
        # Simple heuristic: intervene if analysis mentions "risk" or "significant"
        text = analysis.get('analysis', '').lower()
        should_intervene = 'risk' in text or 'significant' in text
        
        return {
            "status": "fallback",
            "should_intervene": should_intervene,
            "confidence": 0.5,
            "reasoning": "Rule-based heuristic (no LLM available)",
            "recommended_actions": ["Monitor situation"] if should_intervene else [],
            "model": "rule-based"
        }
    
    def _fallback_potential_extraction(self, text) -> Dict[str, Any]:
        """Fallback potential field extraction."""
        # Simple keyword-based extraction
        attractors = []
        barriers = []
        
        text_lower = text.lower()
        
        if 'bullish' in text_lower or 'growth' in text_lower:
            attractors.append({
                "description": "Bullish target",
                "strength": 0.5,
                "target": {"level": "L2", "domain": "tech", "stance": 0.7, "intent": 0.5}
            })
        
        if 'risk' in text_lower or 'avoid' in text_lower:
            barriers.append({
                "description": "Risk zone",
                "strength": 0.8,
                "target": {"level": "L1", "domain": "finance", "stance": -0.9, "intent": -0.9}
            })
        
        return {
            "status": "fallback",
            "attractors": attractors,
            "barriers": barriers,
            "model": "rule-based"
        }
    
    def _fallback_narrative(self, analysis, entity_name) -> str:
        """Fallback narrative generation."""
        return f"{entity_name} trajectory analyzed. {analysis.get('analysis', 'No significant changes observed.')}"


# ============================================================================
# DEMO
# ============================================================================

def demo_llm_agent():
    """Demonstrate LLM agent capabilities."""
    print("\n" + "="*70)
    print("🤖 LLM AGENT DEMO")
    print("="*70 + "\n")
    
    # Initialize agent
    agent = LLMAgent(model="gpt-4")
    
    if not agent.available:
        print("⚠️  LLM unavailable. Showing fallback behavior.\n")
    
    # Sample trajectory data
    initial_state = {
        "level": "L2",
        "domain": "tech",
        "stance": "bullish",
        "intent": "constructive"
    }
    
    final_state = {
        "level": "L1",
        "domain": "tech",
        "stance": "bearish",
        "intent": "neutral"
    }
    
    trajectory_stats = {
        "distance": 2.34,
        "drift": 1.87,
        "volatility": 0.45
    }
    
    # Test 1: Trajectory Analysis
    print("=" * 70)
    print("TEST 1: Trajectory Analysis")
    print("=" * 70)
    
    analysis = agent.analyze_trajectory(
        initial_state=initial_state,
        final_state=final_state,
        trajectory_stats=trajectory_stats,
        entity_context="NVIDIA stock amid GPU shortage concerns"
    )
    
    print(f"\nStatus: {analysis['status']}")
    print(f"Model: {analysis.get('model', 'N/A')}")
    print(f"\nAnalysis:\n{analysis['analysis']}")
    
    # Test 2: Intervention Decision
    print("\n" + "=" * 70)
    print("TEST 2: Intervention Decision")
    print("=" * 70)
    
    decision = agent.decide_intervention(analysis)
    
    print(f"\nShould intervene: {decision.get('should_intervene', False)}")
    print(f"Confidence: {decision.get('confidence', 0):.2f}")
    print(f"Reasoning: {decision.get('reasoning', 'N/A')}")
    
    if decision.get('recommended_actions'):
        print("\nRecommended actions:")
        for action in decision['recommended_actions']:
            print(f"  - {action}")
    
    # Test 3: Potential Field Extraction
    print("\n" + "=" * 70)
    print("TEST 3: Potential Field Extraction")
    print("=" * 70)
    
    strategy_text = """
    Goal: Maintain bullish momentum in AI sector while managing overvaluation risk.
    Avoid: Excessive exposure to shadow actors and hidden agendas.
    Opportunity: Capture upside from infrastructure buildout.
    Risk: Market correction if sentiment shifts bearish.
    """
    
    field_spec = agent.extract_potential_field(strategy_text)
    
    print(f"\nAttractors: {len(field_spec.get('attractors', []))}")
    for attr in field_spec.get('attractors', []):
        print(f"  - {attr.get('description', 'N/A')} (strength: {attr.get('strength', 0):.2f})")
    
    print(f"\nBarriers: {len(field_spec.get('barriers', []))}")
    for barr in field_spec.get('barriers', []):
        print(f"  - {barr.get('description', 'N/A')} (strength: {barr.get('strength', 0):.2f})")
    
    # Test 4: Narrative Generation
    print("\n" + "=" * 70)
    print("TEST 4: Narrative Generation")
    print("=" * 70)
    
    narrative = agent.generate_narrative(analysis, "NVIDIA")
    
    print(f"\nNarrative:\n{narrative}")
    
    print("\n" + "="*70)
    print("✅ LLM Agent demo completed!")
    print("="*70)


if __name__ == "__main__":
    demo_llm_agent()
