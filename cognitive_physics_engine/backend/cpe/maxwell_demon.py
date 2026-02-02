"""
Maxwell's Demon Console - Real-time Cognitive State Visualization
==================================================================

MODULE 3: THE MAXWELL'S DEMON CONSOLE

Real-time monitoring dashboard for cognitive collapse

Author: Raywu Paradigm Implementation Team
Date: 2026-02-01
"""

import numpy as np
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json
from datetime import datetime


@dataclass
class LoopSnapshot:
    """Snapshot of cognitive state at each loop"""
    loop_id: int
    timestamp: str
    status: str
    entropy: float
    consensus_strength: float
    
    # Agent metrics
    avg_logic_score: float
    avg_confidence: float
    max_friction: float
    shadow_weight: float
    
    # Geometric metrics
    mean_position: List[float]
    dispersion: float
    
    # Events
    events: List[str]


class MaxwellDemon:
    """
    Maxwell's Demon: Observer and controller of cognitive collapse
    
    Capabilities:
    1. Real-time state monitoring
    2. Entropy tracking
    3. User command injection
    4. Anomaly detection
    5. Holographic decoding
    """
    
    def __init__(self):
        self.snapshots: List[LoopSnapshot] = []
        self.alerts: List[str] = []
        
    def capture_snapshot(self, engine) -> LoopSnapshot:
        """Capture current state snapshot"""
        from deep_state_agent import CollapseStatus
        
        # Compute metrics
        avg_logic = np.mean([a.logic_score for a in engine.agents])
        avg_conf = np.mean([a.confidence for a in engine.agents])
        max_friction = max([a.compute_friction_score() for a in engine.agents])
        shadow_weight = max([a.hidden_agenda_weight for a in engine.agents])
        
        # Geometric metrics
        positions = np.array([a.lattice.to_vector() for a in engine.agents])
        mean_pos = positions.mean(axis=0)
        dispersion = np.std(positions, axis=0).mean()
        
        # Compute consensus strength
        stances = [a.lattice.x_coord for a in engine.agents if a.role.value != "W"]
        consensus_strength = 1.0 - np.std(stances) if len(stances) > 0 else 0.0
        
        # Status
        status = engine.status_history[-1].value if engine.status_history else "INIT"
        entropy = engine.entropy_history[-1] if engine.entropy_history else 0.0
        
        # Detect events
        events = []
        if entropy > 1.0:
            events.append("⚠️ HIGH ENTROPY: Agents diverging")
        if max_friction > 80:
            events.append("🔥 HIGH FRICTION: Disconnected from reality")
        if shadow_weight > 0.7:
            events.append("👁️ SHADOW DETECTED: Hidden agenda active")
        if consensus_strength > 0.8:
            events.append("✅ CONSENSUS FORMING")
        
        snapshot = LoopSnapshot(
            loop_id=engine.loop_count,
            timestamp=datetime.now().isoformat(),
            status=status,
            entropy=entropy,
            consensus_strength=consensus_strength,
            avg_logic_score=avg_logic,
            avg_confidence=avg_conf,
            max_friction=max_friction,
            shadow_weight=shadow_weight,
            mean_position=mean_pos.tolist(),
            dispersion=dispersion,
            events=events
        )
        
        self.snapshots.append(snapshot)
        return snapshot
    
    def render_console(self) -> str:
        """
        Render Maxwell's Demon console output
        
        MODULE 3: Real-time monitoring dashboard
        """
        if not self.snapshots:
            return "[MAXWELL'S DEMON] No data yet"
        
        latest = self.snapshots[-1]
        
        output = []
        output.append("=" * 80)
        output.append("👁️  MAXWELL'S DEMON CONSOLE v11.0")
        output.append("=" * 80)
        
        # Header
        output.append(f"\n⏰ Loop #{latest.loop_id} | {latest.timestamp}")
        output.append(f"📊 Status: {latest.status}")
        
        # Entropy flow
        output.append(f"\n🌀 ENTROPY FLOW:")
        if len(self.snapshots) >= 5:
            recent = self.snapshots[-5:]
            entropy_trend = " → ".join([f"{s.entropy:.2f}" for s in recent])
            output.append(f"   {entropy_trend}")
        else:
            output.append(f"   {latest.entropy:.3f}")
        
        # Consensus meter
        output.append(f"\n🎯 CONSENSUS STRENGTH: {latest.consensus_strength:.1%}")
        bar_length = int(latest.consensus_strength * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        output.append(f"   [{bar}]")
        
        # Agent metrics
        output.append(f"\n🤖 AGENT METRICS:")
        output.append(f"   Logic Score:  {latest.avg_logic_score:.1f}/100")
        output.append(f"   Confidence:   {latest.avg_confidence:.1%}")
        output.append(f"   Max Friction: {latest.max_friction:.1f}/100")
        output.append(f"   Shadow Weight: {latest.shadow_weight:.1%}")
        
        # Geometric metrics
        output.append(f"\n📐 GEOMETRIC STATE:")
        output.append(f"   Dispersion: {latest.dispersion:.3f}")
        output.append(f"   Mean Position: [{', '.join([f'{x:.2f}' for x in latest.mean_position])}]")
        
        # Events
        if latest.events:
            output.append(f"\n⚡ EVENTS:")
            for event in latest.events:
                output.append(f"   {event}")
        
        # Commands
        output.append(f"\n💻 AVAILABLE COMMANDS:")
        output.append(f"   /inject <evidence>  - Inject new evidence")
        output.append(f"   /tilt bull|bear     - Artificially tilt stance")
        output.append(f"   /shadow             - Reveal shadow agents")
        output.append(f"   /friction +|-       - Increase/decrease friction")
        output.append(f"   /audit              - Full state audit")
        output.append(f"   /nuke               - Reset and restart")
        
        output.append("\n" + "=" * 80)
        
        return "\n".join(output)
    
    def holographic_decode(self, engine, layer: int = 3) -> Dict[str, Any]:
        """
        MODULE 4: HOLOGRAPHIC DECODER
        
        Progressive disclosure of cognitive state
        
        Layers:
        0 - Alert (warnings only)
        1 - Aha Moment (key insight)
        2 - Framework (structure)
        3 - Deep Analysis (full picture)
        4 - Next Steps (recommendations)
        """
        if not self.snapshots:
            return {"error": "No data"}
        
        latest = self.snapshots[-1]
        
        result = {
            "layer": layer,
            "timestamp": latest.timestamp,
            "loop": latest.loop_id
        }
        
        # Layer 0: Alerts
        if latest.events:
            result["layer_0_alerts"] = latest.events
        
        if layer < 1:
            return result
        
        # Layer 1: Aha Moment
        if latest.status == "COLLAPSED":
            aha = "🎯 Cognitive collapse achieved! Consensus has formed."
        elif latest.status == "STAGNANT":
            aha = "⚠️ System is stagnant. Need external input or evidence."
        elif latest.status == "DECEPTIVE":
            aha = "👁️ Shadow agents detected. Hidden agendas at play."
        elif latest.entropy > 1.0:
            aha = "🌀 High entropy - agents are exploring divergent paths."
        else:
            aha = "🔄 System is converging toward consensus."
        
        result["layer_1_aha"] = aha
        
        if layer < 2:
            return result
        
        # Layer 2: Framework
        framework = {
            "cognitive_state": latest.status,
            "entropy_level": "HIGH" if latest.entropy > 1.0 else "MEDIUM" if latest.entropy > 0.5 else "LOW",
            "consensus_formation": "STRONG" if latest.consensus_strength > 0.7 else "WEAK",
            "reality_anchor": "STRONG" if latest.max_friction < 60 else "WEAK",
            "shadow_influence": "HIGH" if latest.shadow_weight > 0.6 else "LOW"
        }
        result["layer_2_framework"] = framework
        
        if layer < 3:
            return result
        
        # Layer 3: Deep Analysis
        agent_profiles = []
        for agent in engine.agents:
            profile = {
                "id": agent.id,
                "role": agent.role.value,
                "belief": agent.belief,
                "confidence": agent.confidence,
                "logic_score": agent.logic_score,
                "friction": agent.compute_friction_score(),
                "position": agent.lattice.to_vector().tolist()
            }
            agent_profiles.append(profile)
        
        result["layer_3_agents"] = agent_profiles
        
        # Trajectory analysis
        if len(self.snapshots) > 1:
            entropy_trend = [s.entropy for s in self.snapshots[-5:]]
            consensus_trend = [s.consensus_strength for s in self.snapshots[-5:]]
            
            result["layer_3_trajectory"] = {
                "entropy_trend": entropy_trend,
                "consensus_trend": consensus_trend,
                "converging": entropy_trend[-1] < entropy_trend[0]
            }
        
        if layer < 4:
            return result
        
        # Layer 4: Next Steps
        recommendations = []
        
        if latest.status == "STAGNANT":
            recommendations.append("Inject new evidence with /inject command")
            recommendations.append("Consider exploring shadow hypotheses with /shadow")
        elif latest.status == "DECEPTIVE":
            recommendations.append("Reveal shadow agents with /shadow")
            recommendations.append("Increase fact density in evidence chain")
        elif latest.entropy > 1.0:
            recommendations.append("Allow more loops for convergence")
            recommendations.append("Consider tilting toward stronger evidence")
        elif latest.consensus_strength > 0.8:
            recommendations.append("System is ready to collapse - extract final consensus")
        
        result["layer_4_next_steps"] = recommendations
        
        return result
    
    def export_timeline(self) -> List[Dict]:
        """Export full timeline for visualization"""
        return [
            {
                "loop": s.loop_id,
                "entropy": s.entropy,
                "consensus": s.consensus_strength,
                "status": s.status,
                "events": s.events
            }
            for s in self.snapshots
        ]
    
    def detect_anomalies(self) -> List[str]:
        """Detect system anomalies"""
        anomalies = []
        
        if not self.snapshots or len(self.snapshots) < 3:
            return anomalies
        
        recent = self.snapshots[-3:]
        
        # Check for oscillation
        entropies = [s.entropy for s in recent]
        if max(entropies) - min(entropies) > 0.5:
            anomalies.append("🌊 OSCILLATION: Entropy is unstable")
        
        # Check for runaway shadow
        shadows = [s.shadow_weight for s in recent]
        if all(s > 0.8 for s in shadows):
            anomalies.append("👻 SHADOW TAKEOVER: Shadow agents dominating")
        
        # Check for confidence collapse
        confidences = [s.avg_confidence for s in recent]
        if all(c < 0.3 for c in confidences):
            anomalies.append("😰 CONFIDENCE COLLAPSE: No agent trusts their belief")
        
        return anomalies


# ==================== DEMO ====================

if __name__ == "__main__":
    print("Testing Maxwell's Demon Console\n")
    
    # Import engine
    import sys
    sys.path.insert(0, '.')
    from deep_state_agent import DeepStateEngine
    
    # Initialize
    engine = DeepStateEngine()
    demon = MaxwellDemon()
    
    # Run simulation
    question = "Should we invest in quantum computing stocks now?"
    engine.initialize_lattices(question, domains=["tech", "finance"])
    engine.spawn_agents()
    
    # Simulate a few loops manually
    for _ in range(5):
        engine.loop_count += 1
        
        # Update agent states (simplified)
        for agent in engine.agents:
            agent.confidence += np.random.randn() * 0.05
            agent.logic_score = max(0, agent.logic_score + np.random.randn() * 5)
        
        # Compute entropy
        positions = np.array([a.lattice.to_vector() for a in engine.agents])
        entropy = np.std(positions, axis=0).mean()
        engine.entropy_history.append(entropy)
        
        from deep_state_agent import CollapseStatus
        engine.status_history.append(CollapseStatus.CONVERGING)
        
        # Capture snapshot
        snapshot = demon.capture_snapshot(engine)
        
        # Render console
        print(demon.render_console())
        print("\n")
    
    # Holographic decode
    print("\n" + "=" * 80)
    print("HOLOGRAPHIC DECODER - LAYER 4 (Full Analysis)")
    print("=" * 80)
    decoded = demon.holographic_decode(engine, layer=4)
    print(json.dumps(decoded, indent=2, default=str))
    
    print("\n✅ Maxwell's Demon Console test completed")
