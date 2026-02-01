"""
WorldOS Engine - The Core Game Loop
====================================

This is the heart of Raywu WorldOS. It orchestrates:
1. Reading state from Markdown (The Body)
2. Simulating physics (The Math)  
3. Calling LLM for decisions (The Mind)
4. Writing results back (The State)

Philosophy:
- World runs in discrete ticks (like a game engine)
- Each tick: READ → SIMULATE → DECIDE → WRITE
- State persistence ensures continuity across sessions

Architecture:
    ┌─────────────┐
    │  Markdown   │ ← Read state
    │   Database  │
    └──────┬──────┘
           ↓
    ┌─────────────┐
    │   Physics   │ ← Evolve dynamics
    │   Engine    │
    └──────┬──────┘
           ↓
    ┌─────────────┐
    │    LLM      │ ← Decide interventions
    │  Reasoning  │
    └──────┬──────┘
           ↓
    ┌─────────────┐
    │  Markdown   │ ← Write updates
    │   Database  │
    └─────────────┘

Author: Raywu WorldOS Team
Date: 2026-02-01
Version: v61.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "kernel"))
sys.path.insert(0, str(Path(__file__).parent / "brain"))
sys.path.insert(0, str(Path(__file__).parent / "storage"))

import time
import numpy as np
from typing import Dict, List, Optional, Any

from manifold import CognitiveManifold
from dynamics import PhysicsEngine, PotentialField
from translator import NeuroSymbolicTranslator
from markdown_db import MarkdownDB


class WorldOS:
    """
    The Operating System for Cognitive Physics.
    
    This class manages the complete simulation loop:
    - State persistence (Markdown files)
    - Physics simulation (manifold dynamics)
    - Cognitive interventions (LLM reasoning)
    """
    
    def __init__(self, 
                 world_state_dir: str = "world_state",
                 gamma: float = 0.3,
                 sigma: float = 0.05,
                 tick_duration: float = 1.0):
        """
        Initialize WorldOS.
        
        Args:
            world_state_dir: Directory for Markdown database
            gamma: Friction coefficient for physics
            sigma: Noise intensity for physics
            tick_duration: Duration of each physics tick (in time units)
        """
        print("\n" + "="*70)
        print("🌍 WORLDOS INITIALIZATION")
        print("="*70 + "\n")
        
        # Core components
        print("  Initializing manifold...")
        self.manifold = CognitiveManifold()
        
        print("  Initializing physics engine...")
        self.physics = PhysicsEngine(self.manifold, gamma=gamma, sigma=sigma)
        
        print("  Initializing translator...")
        self.translator = NeuroSymbolicTranslator(self.manifold)
        
        print("  Initializing database...")
        self.db = MarkdownDB(root_dir=world_state_dir)
        
        print("  Initializing potential field...")
        self.potential = PotentialField()
        
        self.tick_duration = tick_duration
        self.tick_count = 0
        
        print("\n✓ WorldOS ready!")
        print("="*70 + "\n")
    
    def add_entity_from_markdown(self, entity_id: str):
        """
        Load entity from Markdown and add to active simulation.
        
        Args:
            entity_id: Entity identifier in database
        """
        entity = self.db.read_entity(entity_id)
        
        if not entity:
            print(f"⚠️  Entity '{entity_id}' not found in database")
            return None
        
        # Read from database
        metadata = entity['metadata']
        
        # Encode to manifold
        point = self.manifold.encode_state(
            level=self._parse_level(metadata.get('level', 'L3')),
            domain=metadata.get('domain', 'tech'),
            stance=float(metadata.get('stance', 0.0)),
            intent=float(metadata.get('intent', 0.0)),
            time=float(metadata.get('time', 0.0)),
            scale=float(metadata.get('scale', 0.0))
        )
        
        return point
    
    def _parse_level(self, level_str: str) -> int:
        """Parse level string (e.g., 'L3') to integer."""
        if isinstance(level_str, str) and level_str.startswith('L'):
            return int(level_str[1])
        return 3
    
    def tick(self, 
             entity_id: str, 
             context: Optional[Dict[str, Any]] = None,
             llm_intervention: bool = False) -> Dict[str, Any]:
        """
        Execute one simulation tick for an entity.
        
        Process:
        1. READ: Load entity state from Markdown
        2. SIMULATE: Evolve physics for tick_duration
        3. DECIDE: (Optional) Call LLM for intervention
        4. WRITE: Save updated state back to Markdown
        
        Args:
            entity_id: Entity to simulate
            context: Additional context for LLM
            llm_intervention: Whether to call LLM this tick
        
        Returns:
            Dictionary with tick results
        """
        self.tick_count += 1
        
        print(f"\n{'='*70}")
        print(f"⏰ TICK #{self.tick_count} - Entity: {entity_id}")
        print(f"{'='*70}\n")
        
        # ====================================================================
        # STEP 1: READ STATE FROM MARKDOWN
        # ====================================================================
        print("📖 [1/4] READ: Loading state from Markdown...")
        
        initial_point = self.add_entity_from_markdown(entity_id)
        
        if initial_point is None:
            return {"status": "error", "message": f"Entity {entity_id} not found"}
        
        print(f"  ✓ State loaded: {initial_point[:4]}... (first 4 dims)")
        
        # ====================================================================
        # STEP 2: SIMULATE PHYSICS
        # ====================================================================
        print("\n⚙️  [2/4] SIMULATE: Running physics evolution...")
        
        start_time = time.time()
        
        final_point, trajectory = self.physics.evolve(
            initial_state=initial_point,
            time_span=(0.0, self.tick_duration),
            potential=self.potential,
            dt=0.02  # Fine timestep for accuracy
        )
        
        elapsed = time.time() - start_time
        
        distance = self.manifold.metric.dist(initial_point, final_point)
        
        print(f"  ✓ Evolution complete ({elapsed:.3f}s)")
        print(f"  ✓ Trajectory: {len(trajectory)} points")
        print(f"  ✓ Cognitive distance: {distance:.4f}")
        
        # ====================================================================
        # STEP 3: DECIDE (LLM INTERVENTION)
        # ====================================================================
        print("\n🧠 [3/4] DECIDE: Cognitive processing...")
        
        intervention_made = False
        llm_decision = None
        
        if llm_intervention:
            # This is where we would call GPT-4 to analyze the trajectory
            # and decide on interventions
            # For now, we'll use rule-based logic as a placeholder
            
            decoded_initial = self.manifold.decode_state(initial_point)
            decoded_final = self.manifold.decode_state(final_point)
            
            print(f"  Initial: Level={decoded_initial['level']}, "
                  f"Stance={decoded_initial['stance']}")
            print(f"  Final:   Level={decoded_final['level']}, "
                  f"Stance={decoded_final['stance']}")
            
            # Simple rule: If moved significantly, flag it
            if distance > 1.0:
                intervention_made = True
                llm_decision = "Significant movement detected. Monitoring closely."
                print(f"  ⚠️  Intervention: {llm_decision}")
        else:
            print("  ⏭️  Skipped (llm_intervention=False)")
        
        # ====================================================================
        # STEP 4: WRITE RESULTS BACK TO MARKDOWN
        # ====================================================================
        print("\n💾 [4/4] WRITE: Saving state to Markdown...")
        
        # Decode final state
        decoded = self.manifold.decode_state(final_point)
        
        # Update metadata (keep numeric values)
        updates = {
            'level': decoded['level'],
            'domain': decoded['domain'],
            'stance': decoded['coordinates'][6],  # Keep raw numeric
            'intent': decoded['coordinates'][7],   # Keep raw numeric
            'time': decoded['coordinates'][8],     # Keep raw numeric
            'scale': decoded['coordinates'][9],    # Keep raw numeric
            'coordinates': decoded['coordinates']
        }
        
        # Log message
        log_message = f"""Physics tick #{self.tick_count} completed:
- Duration: {self.tick_duration} time units
- Cognitive distance: {distance:.4f}
- Final state: Level {decoded['level']}, {decoded['stance']} stance
"""
        
        if intervention_made:
            log_message += f"- LLM Decision: {llm_decision}\n"
        
        # Write to database
        self.db.update_entity(entity_id, updates, log_message)
        
        print("  ✓ State saved to database")
        
        # ====================================================================
        # RETURN SUMMARY
        # ====================================================================
        print(f"\n{'='*70}")
        print(f"✅ TICK #{self.tick_count} COMPLETED")
        print(f"{'='*70}\n")
        
        return {
            'status': 'success',
            'tick': self.tick_count,
            'entity_id': entity_id,
            'initial_state': initial_point,
            'final_state': final_point,
            'trajectory': trajectory,
            'distance': distance,
            'decoded': decoded,
            'intervention': intervention_made,
            'llm_decision': llm_decision,
            'elapsed_time': elapsed
        }
    
    def run_episode(self, 
                    entity_id: str, 
                    num_ticks: int = 10,
                    llm_frequency: int = 3) -> List[Dict[str, Any]]:
        """
        Run multiple ticks (an episode).
        
        Args:
            entity_id: Entity to simulate
            num_ticks: Number of ticks to run
            llm_frequency: Call LLM every N ticks
        
        Returns:
            List of tick results
        """
        print("\n" + "="*70)
        print(f"🎬 EPISODE START: {entity_id}")
        print(f"   Ticks: {num_ticks}, LLM frequency: every {llm_frequency} ticks")
        print("="*70 + "\n")
        
        results = []
        
        for i in range(num_ticks):
            # Decide if LLM should intervene this tick
            llm_this_tick = (i % llm_frequency == 0)
            
            # Run tick
            result = self.tick(entity_id, llm_intervention=llm_this_tick)
            results.append(result)
            
            # Brief pause between ticks
            time.sleep(0.1)
        
        print("\n" + "="*70)
        print(f"🎬 EPISODE COMPLETE: {entity_id}")
        print(f"   Total ticks: {len(results)}")
        print("="*70 + "\n")
        
        return results


# ============================================================================
# DEMO
# ============================================================================

def demo_worldos():
    """Demonstrate WorldOS tick system."""
    print("\n" + "="*70)
    print("🌍 WORLDOS ENGINE DEMO")
    print("="*70 + "\n")
    
    # Initialize WorldOS
    world = WorldOS(world_state_dir="demo_world_state", tick_duration=1.0)
    
    # First, ensure we have an entity to simulate
    # (Reuse from markdown_db demo if it exists, or create new)
    nvidia = world.db.read_entity("nvidia")
    
    if not nvidia:
        print("📝 Creating demo entity: nvidia")
        world.db.write_entity(
            entity_id="nvidia",
            metadata={
                "level": "L2",
                "domain": "tech",
                "stance": 0.6,
                "intent": 0.8,
                "time": 0.3,
                "scale": 0.2
            },
            body="# NVIDIA\n\n## State\nBullish tech stock."
        )
    
    # Add attractor to create interesting dynamics
    target_point = world.manifold.encode_state(2, 'tech', 0.8, 0.7, 0.5, 0.0)
    world.potential.add_attractor(target_point, strength=0.5, radius=1.5)
    print("✓ Added attractor (bullish tech region)")
    
    # Run single tick
    print("\n" + "-"*70)
    print("DEMO 1: Single Tick")
    print("-"*70)
    
    result = world.tick("nvidia", llm_intervention=True)
    
    print(f"\nResult:")
    print(f"  Status: {result['status']}")
    print(f"  Distance traveled: {result['distance']:.4f}")
    print(f"  Final level: {result['decoded']['level']}")
    print(f"  Final stance: {result['decoded']['stance']}")
    
    # Run short episode
    print("\n" + "-"*70)
    print("DEMO 2: Short Episode (5 ticks)")
    print("-"*70)
    
    episode_results = world.run_episode("nvidia", num_ticks=5, llm_frequency=2)
    
    print(f"\nEpisode summary:")
    print(f"  Total ticks: {len(episode_results)}")
    
    total_distance = sum(r['distance'] for r in episode_results)
    print(f"  Total distance: {total_distance:.4f}")
    
    interventions = sum(1 for r in episode_results if r['intervention'])
    print(f"  LLM interventions: {interventions}")
    
    # Create snapshot
    print("\n📸 Creating world state snapshot...")
    snapshot_path = world.db.create_snapshot(
        f"After WorldOS demo: {len(episode_results)} ticks simulated"
    )
    print(f"  Saved: {snapshot_path}")
    
    print("\n" + "="*70)
    print("✅ WorldOS demo completed!")
    print("="*70)


if __name__ == "__main__":
    demo_worldos()
