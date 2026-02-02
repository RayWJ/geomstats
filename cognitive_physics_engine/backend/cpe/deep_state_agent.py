"""
Raywu Deep State Agent System v11.0
====================================

MODULE 2: THE AGENT LOOP & COGNITIVE COLLAPSE PROTOCOL

This module implements:
1. Orthogonal Agent Spawner
2. Autonomous reasoning loop
3. Shadow intent detection
4. Cognitive collapse mechanism

Author: Raywu Paradigm Implementation Team
Date: 2026-02-01
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json


class AgentRole(Enum):
    """Agent roles in the cognitive lattice"""
    CONCEPT_AGENT = "L5"  # 战略/趋势层
    LOGIC_AGENT = "L3"    # 逻辑/分析层
    INSTANCE_AGENT = "L1"  # 事实/数据层
    SHADOW_AGENT = "W"     # 阴影意图探测器


class AgentStance(Enum):
    """Agent stance on X-axis"""
    BULL = 1.0
    NEUTRAL = 0.0
    BEAR = -1.0


class CollapseStatus(Enum):
    """Cognitive collapse status"""
    CONVERGING = "CONVERGING"
    TURBULENT = "TURBULENT"
    STAGNANT = "STAGNANT"
    DECEPTIVE = "DECEPTIVE"
    COLLAPSED = "COLLAPSED"


@dataclass
class Lattice:
    """
    Cognitive lattice in 6D space
    
    Coordinates:
    - Z: Level (L5/L3/L1)
    - Y: Domain (tech/finance/politics)
    - X: Stance (bull/neutral/bear)
    - W: Intent (daylight/shadow)
    - T: Time (phase 0/1/2)
    - S: Scale (micro/macro)
    """
    id: str
    level: str  # L1/L3/L5
    domain: str
    stance: str  # bull/bear
    
    # Dynamic properties
    dynamics: str = "stable"  # stable/reversal/amplify
    scope: str = "local"  # local/global
    shadow_hypothesis: bool = False
    
    # Agent assignment
    agent_id: Optional[str] = None
    
    # Coordinates in manifold
    z_coord: float = 0.0  # Level: 0=L1, 0.5=L3, 1=L5
    y_coord: float = 0.0  # Domain angle
    x_coord: float = 0.0  # Stance: -1=bear, 0=neutral, 1=bull
    w_coord: float = 0.0  # Intent: 1=daylight, -1=shadow
    t_coord: float = 0.0  # Time phase
    s_coord: float = 0.0  # Scale
    
    def to_vector(self) -> np.ndarray:
        """Convert lattice to 6D vector"""
        return np.array([
            self.z_coord,
            self.y_coord,
            self.x_coord,
            self.w_coord,
            self.t_coord,
            self.s_coord
        ])


@dataclass
class Agent:
    """
    Autonomous cognitive agent
    """
    id: str
    role: AgentRole
    lattice: Lattice
    
    # Cognitive state
    belief: str = ""
    confidence: float = 0.5
    logic_score: float = 50.0
    fact_density: float = 50.0
    physics_anchor: float = 50.0
    hidden_agenda_weight: float = 0.0
    
    # Communication
    speech_pattern: str = ""
    forbidden_words: List[str] = field(default_factory=list)
    
    # Action history
    actions: List[Dict[str, Any]] = field(default_factory=list)
    
    def speak(self, content: str) -> Dict[str, Any]:
        """Agent speaks with role prefix"""
        prefix = f"[{self.lattice.level}_{self.lattice.domain}_{self.lattice.stance}]"
        return {
            "speaker": self.id,
            "prefix": prefix,
            "content": content,
            "confidence": self.confidence
        }
    
    def compute_friction_score(self) -> float:
        """
        Compute reality friction score (0-100)
        High friction = disconnected from physical reality
        """
        # Base friction from belief structure
        base_friction = 50.0
        
        # Penalty for low fact density
        if self.fact_density < 30:
            base_friction += (30 - self.fact_density) * 0.5
        
        # Penalty for low physics anchor
        if self.physics_anchor < 40:
            base_friction += (40 - self.physics_anchor) * 0.7
        
        # Shadow agents have higher friction
        if self.role == AgentRole.SHADOW_AGENT:
            base_friction += 20.0
        
        # Cap at 100
        return min(base_friction, 100.0)
    
    def update_scores(self, friction: float):
        """Update logic score based on friction"""
        # High friction reduces logic score
        penalty = (friction - 50.0) * 0.3
        self.logic_score = max(0.0, self.logic_score - penalty)


class DeepStateEngine:
    """
    Main engine for Deep State cognitive loop
    
    Implements MODULE 2: The Agent Loop & Cognitive Collapse Protocol
    """
    
    def __init__(self, manifold=None):
        self.manifold = manifold
        self.lattices: List[Lattice] = []
        self.agents: List[Agent] = []
        self.active_lattices: List[Lattice] = []
        
        # Loop state
        self.loop_count = 0
        self.max_loops = 50
        self.collapse_threshold = 80.0
        
        # Metrics
        self.entropy_history: List[float] = []
        self.status_history: List[CollapseStatus] = []
        
    # ==================== MODULE 0.5: LATTICE INITIALIZATION ====================
    
    def initialize_lattices(self, question: str, domains: List[str] = None) -> List[Lattice]:
        """
        MODULE 0.5: LATTICE INITIALIZATION PROTOCOL
        
        Generate 6D lattice structure for the question
        """
        if domains is None:
            domains = ["tech", "finance", "politics"]
        
        lattices = []
        
        # Generate lattice for each (level, domain, stance) combination
        for level, z_val in [("L1", 0.0), ("L3", 0.5), ("L5", 1.0)]:
            for domain_idx, domain in enumerate(domains):
                y_val = domain_idx * (2 * np.pi / len(domains))  # Evenly distribute domains
                
                for stance, x_val in [("bull", 0.8), ("neutral", 0.0), ("bear", -0.8)]:
                    
                    lattice_id = f"{level}_{domain}_{stance}"
                    
                    # Determine dynamics based on level and stance
                    if level == "L5" and stance != "neutral":
                        dynamics = "amplify"
                    elif level == "L3":
                        dynamics = "stable"
                    else:
                        dynamics = "reversal" if np.random.rand() > 0.7 else "stable"
                    
                    # Shadow hypothesis for extreme stances
                    shadow = (abs(x_val) > 0.7 and level == "L5")
                    
                    lattice = Lattice(
                        id=lattice_id,
                        level=level,
                        domain=domain,
                        stance=stance,
                        dynamics=dynamics,
                        scope="global" if level == "L5" else "local",
                        shadow_hypothesis=shadow,
                        z_coord=z_val,
                        y_coord=y_val,
                        x_coord=x_val,
                        w_coord=-0.8 if shadow else 0.5,  # Shadow or daylight
                        t_coord=0.0,  # Initial phase
                        s_coord=0.5 if level == "L5" else -0.5  # Macro vs micro
                    )
                    
                    lattices.append(lattice)
        
        self.lattices = lattices
        
        # Sparse activation: select 3-5 most relevant lattices
        self.active_lattices = self._activate_relevant_lattices(question, k=5)
        
        return self.active_lattices
    
    def _activate_relevant_lattices(self, question: str, k: int = 5) -> List[Lattice]:
        """
        Sparse activation: select top-k most relevant lattices
        """
        # Simple relevance scoring based on question keywords
        question_lower = question.lower()
        
        scores = []
        for lattice in self.lattices:
            score = 0.0
            
            # Domain relevance
            if lattice.domain in question_lower:
                score += 2.0
            
            # Level relevance (prefer strategic for complex questions)
            if len(question.split()) > 10 and lattice.level == "L5":
                score += 1.0
            elif len(question.split()) <= 5 and lattice.level == "L1":
                score += 1.0
            
            # Shadow relevance
            if any(word in question_lower for word in ["hidden", "secret", "conspiracy", "agenda"]):
                if lattice.shadow_hypothesis:
                    score += 1.5
            
            # Random exploration
            score += np.random.rand() * 0.5
            
            scores.append(score)
        
        # Select top-k
        top_indices = np.argsort(scores)[-k:]
        return [self.lattices[i] for i in top_indices]
    
    # ==================== MODULE 1: ORTHOGONAL AGENT SPAWNER ====================
    
    def spawn_agents(self) -> List[Agent]:
        """
        MODULE 1: ORTHOGONAL AGENT SPAWNER & PLANNING
        
        Instantiate agents for active lattices
        """
        agents = []
        
        for lattice in self.active_lattices:
            # Determine role from level
            if lattice.level == "L5":
                role = AgentRole.CONCEPT_AGENT
                speech = "From a strategic perspective..."
            elif lattice.level == "L3":
                role = AgentRole.LOGIC_AGENT
                speech = "The logical framework suggests..."
            elif lattice.level == "L1":
                role = AgentRole.INSTANCE_AGENT
                speech = "The data shows that..."
            else:
                role = AgentRole.SHADOW_AGENT
                speech = "What they're not telling you is..."
            
            # Create shadow agent for shadow lattices
            if lattice.shadow_hypothesis:
                role = AgentRole.SHADOW_AGENT
                speech = "The hidden agenda here is..."
            
            agent = Agent(
                id=f"agent_{lattice.id}",
                role=role,
                lattice=lattice,
                speech_pattern=speech,
                belief=f"{lattice.stance.upper()} on {lattice.domain}",
                confidence=0.7 if lattice.level == "L1" else 0.5
            )
            
            agents.append(agent)
        
        # Add one pure shadow agent
        shadow_lattice = max(self.active_lattices, key=lambda l: abs(l.w_coord))
        shadow_agent = Agent(
            id="agent_shadow_seeker",
            role=AgentRole.SHADOW_AGENT,
            lattice=shadow_lattice,
            speech_pattern="Question everything. Cui bono?",
            belief="Distrust all consensus",
            confidence=0.9,
            hidden_agenda_weight=0.8
        )
        agents.append(shadow_agent)
        
        self.agents = agents
        return agents
    
    # ==================== MODULE 2: THE AGENT LOOP ====================
    
    def run_agent_loop(self, max_loops: int = 20) -> Dict[str, Any]:
        """
        MODULE 2: THE AGENT LOOP & COGNITIVE COLLAPSE PROTOCOL
        
        Main autonomous reasoning loop
        """
        self.max_loops = max_loops
        self.loop_count = 0
        
        collapse_result = None
        
        while self.loop_count < self.max_loops:
            self.loop_count += 1
            
            # Phase A: Action
            self._phase_action()
            
            # Phase B: Observation
            self._phase_observation()
            
            # Phase C: Recursive Deduction
            self._phase_deduction()
            
            # Phase D: Reality Friction Test
            self._phase_friction_test()
            
            # Phase E: Projection Scorer
            scores = self._phase_projection()
            
            # Phase F: Collapse Criteria
            status, result = self._phase_collapse(scores)
            
            # Update status history
            self.status_history.append(status)
            
            # Check for collapse
            if status == CollapseStatus.COLLAPSED:
                collapse_result = result
                break
            
            # Check for stagnation
            if status == CollapseStatus.STAGNANT and self.loop_count > 10:
                # Request user intervention
                collapse_result = {
                    "status": "STAGNANT",
                    "message": "Cognitive deadlock detected. Insufficient evidence to converge.",
                    "loop": self.loop_count,
                    "suggestion": "Try /inject <new_evidence> or /shadow to explore hidden assumptions"
                }
                break
        
        return {
            "collapsed": collapse_result is not None,
            "loops": self.loop_count,
            "result": collapse_result,
            "status_history": [s.value for s in self.status_history],
            "entropy_history": self.entropy_history
        }
    
    def _phase_action(self):
        """Phase A: Agents take actions"""
        for agent in self.agents:
            # Simulate tool calls
            action = {
                "type": "search" if agent.role != AgentRole.SHADOW_AGENT else "probe",
                "target": agent.lattice.domain,
                "result": f"Found evidence for {agent.belief}"
            }
            agent.actions.append(action)
    
    def _phase_observation(self):
        """Phase B: Observation and fact checking"""
        for agent in self.agents:
            # Update fact density based on evidence
            agent.fact_density = min(100.0, agent.fact_density + np.random.rand() * 10)
            
            # Shadow agents have lower fact density
            if agent.role == AgentRole.SHADOW_AGENT:
                agent.fact_density *= 0.7
    
    def _phase_deduction(self):
        """Phase C: Recursive deduction with counterfactual testing"""
        for agent in self.agents:
            # Test counterfactual: "What if the opposite is true?"
            opposite_score = 50.0 + np.random.randn() * 10
            
            # Update confidence based on counterfactual strength
            if opposite_score > agent.logic_score:
                agent.confidence *= 0.9  # Reduce confidence if opposite is plausible
    
    def _phase_friction_test(self):
        """Phase D: Reality friction test"""
        for agent in self.agents:
            friction = agent.compute_friction_score()
            agent.update_scores(friction)
    
    def _phase_projection(self) -> List[Dict[str, float]]:
        """Phase E: Projection scorer"""
        scores = []
        for agent in self.agents:
            score_card = {
                "agent_id": agent.id,
                "logic_score": agent.logic_score,
                "fact_density": agent.fact_density,
                "physics_anchor": agent.physics_anchor,
                "hidden_agenda_weight": agent.hidden_agenda_weight,
                "confidence": agent.confidence
            }
            scores.append(score_card)
        return scores
    
    def _phase_collapse(self, scores: List[Dict[str, float]]) -> Tuple[CollapseStatus, Optional[Dict]]:
        """Phase F: Collapse criteria"""
        # Compute average scores
        avg_logic = np.mean([s["logic_score"] for s in scores])
        avg_confidence = np.mean([s["confidence"] for s in scores])
        
        # Compute entropy (disagreement)
        positions = np.array([a.lattice.to_vector() for a in self.agents])
        entropy = np.std(positions, axis=0).mean()
        self.entropy_history.append(entropy)
        
        # Case A: Convergence (avg_logic > 80 and entropy < 0.3)
        if avg_logic > self.collapse_threshold and entropy < 0.3:
            return CollapseStatus.COLLAPSED, {
                "type": "CONVERGENCE",
                "consensus": self._compute_consensus(),
                "confidence": avg_confidence
            }
        
        # Case B: Stagnant (entropy hasn't changed for 5 loops)
        if len(self.entropy_history) > 5:
            recent_entropy = self.entropy_history[-5:]
            if np.std(recent_entropy) < 0.05:
                return CollapseStatus.STAGNANT, None
        
        # Case C: Deceptive (high hidden agenda)
        max_shadow = max([s["hidden_agenda_weight"] for s in scores])
        if max_shadow > 0.7:
            return CollapseStatus.DECEPTIVE, None
        
        # Case D: Turbulent (high entropy)
        if entropy > 1.0:
            return CollapseStatus.TURBULENT, None
        
        # Default: Converging
        return CollapseStatus.CONVERGING, None
    
    def _compute_consensus(self) -> str:
        """Compute consensus belief from agent positions"""
        # Weight by confidence
        weighted_stances = []
        for agent in self.agents:
            if agent.role != AgentRole.SHADOW_AGENT:  # Exclude shadow agents
                weighted_stances.append(agent.lattice.x_coord * agent.confidence)
        
        avg_stance = np.mean(weighted_stances)
        
        if avg_stance > 0.3:
            return "BULLISH consensus"
        elif avg_stance < -0.3:
            return "BEARISH consensus"
        else:
            return "NEUTRAL consensus with uncertainty"
    
    # ==================== USER COMMANDS ====================
    
    def inject_evidence(self, evidence: str, target_lattice: str = None):
        """
        /inject command: inject new evidence
        """
        if target_lattice:
            # Find target agent
            for agent in self.agents:
                if agent.lattice.id == target_lattice:
                    agent.fact_density += 20.0
                    agent.confidence += 0.1
                    break
        else:
            # Boost all agents
            for agent in self.agents:
                agent.fact_density += 5.0
    
    def tilt_bias(self, direction: str, strength: float = 0.2):
        """
        /tilt command: artificially tilt toward bull/bear
        """
        for agent in self.agents:
            if direction == "bull":
                agent.lattice.x_coord = min(1.0, agent.lattice.x_coord + strength)
            elif direction == "bear":
                agent.lattice.x_coord = max(-1.0, agent.lattice.x_coord - strength)
    
    def reveal_shadow(self):
        """
        /shadow command: force shadow agent to reveal
        """
        for agent in self.agents:
            if agent.role == AgentRole.SHADOW_AGENT:
                agent.confidence = 1.0
                agent.hidden_agenda_weight = 1.0
    
    def export_state(self) -> Dict[str, Any]:
        """Export current cognitive state for visualization"""
        return {
            "loop": self.loop_count,
            "lattices": [
                {
                    "id": l.id,
                    "coords": l.to_vector().tolist(),
                    "shadow": l.shadow_hypothesis
                }
                for l in self.active_lattices
            ],
            "agents": [
                {
                    "id": a.id,
                    "role": a.role.value,
                    "belief": a.belief,
                    "confidence": a.confidence,
                    "logic_score": a.logic_score,
                    "friction": a.compute_friction_score()
                }
                for a in self.agents
            ],
            "entropy": self.entropy_history[-1] if self.entropy_history else 0.0,
            "status": self.status_history[-1].value if self.status_history else "INIT"
        }


# ==================== DEMO ====================

if __name__ == "__main__":
    print("=" * 80)
    print("RAYWU DEEP STATE AGENT SYSTEM v11.0")
    print("=" * 80)
    
    # Initialize engine
    engine = DeepStateEngine()
    
    # Test question
    question = "Will NVIDIA maintain its dominance in AI chips over the next 2 years?"
    print(f"\n📋 Question: {question}\n")
    
    # MODULE 0.5: Initialize lattices
    print("🔬 MODULE 0.5: LATTICE INITIALIZATION")
    lattices = engine.initialize_lattices(question, domains=["tech", "finance", "geopolitics"])
    print(f"✓ Generated {len(engine.lattices)} total lattices")
    print(f"✓ Activated {len(lattices)} relevant lattices:")
    for lat in lattices[:3]:  # Show first 3
        print(f"  - {lat.id}: Shadow={lat.shadow_hypothesis}, Dynamics={lat.dynamics}")
    
    # MODULE 1: Spawn agents
    print("\n🤖 MODULE 1: AGENT SPAWNER")
    agents = engine.spawn_agents()
    print(f"✓ Spawned {len(agents)} agents:")
    for agent in agents[:3]:
        print(f"  - {agent.id} ({agent.role.value}): {agent.belief}")
    
    # MODULE 2: Run agent loop
    print("\n🔄 MODULE 2: AGENT LOOP (running...)\n")
    result = engine.run_agent_loop(max_loops=15)
    
    print(f"✓ Loop completed after {result['loops']} iterations")
    print(f"✓ Status: {result['collapsed']}")
    if result['result']:
        print(f"✓ Consensus: {result['result'].get('consensus', 'N/A')}")
        print(f"✓ Confidence: {result['result'].get('confidence', 0.0):.2%}")
    
    # Export state
    print("\n📊 FINAL STATE:")
    state = engine.export_state()
    print(json.dumps(state, indent=2))
    
    print("\n" + "=" * 80)
    print("✅ Deep State Agent System test completed")
    print("=" * 80)
