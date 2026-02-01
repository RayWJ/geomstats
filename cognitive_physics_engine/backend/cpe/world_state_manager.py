"""
World State Manager - Raywu Cognitive Physics Engine
=====================================================

Bridges ephemeral 6D tensor computations with persistent Markdown world state.
Inspired by OpenClaw's memory system.

Philosophy:
- The world exists as Markdown files (human-readable, LLM-friendly)
- 6D manifold computations are EPHEMERAL (temporary calculation space)
- Results are "collapsed" back into Markdown (quantum → classical)
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import numpy as np

# Try to import frontmatter for YAML metadata parsing
try:
    import frontmatter
    FRONTMATTER_AVAILABLE = True
except ImportError:
    FRONTMATTER_AVAILABLE = False
    print("⚠️  python-frontmatter not available. Install with: pip install python-frontmatter")


class WorldStateManager:
    """
    Manages the persistent world state as a file system of Markdown documents.
    
    Core Philosophy (OpenClaw Style):
    1. World state = Markdown files (not database)
    2. Files are source of truth
    3. Incremental updates (not overwrites)
    4. Human-readable + LLM-friendly
    5. Version control via Git
    """
    
    def __init__(self, world_root: str = "./world_state"):
        """
        Initialize world state manager.
        
        Args:
            world_root: Root directory for world state files
        """
        self.root = Path(world_root)
        self.entities_dir = self.root / "entities"
        self.relations_dir = self.root / "relations"
        self.narratives_dir = self.root / "narratives"
        self.shadows_dir = self.root / "shadows"
        self.memory_dir = self.root / "memory"
        
        # Create directories
        for dir_path in [
            self.entities_dir,
            self.relations_dir,
            self.narratives_dir,
            self.shadows_dir,
            self.memory_dir,
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        print(f"✓ WorldStateManager initialized at: {self.root}")
    
    # ========================================================================
    # READ: World → Tensor
    # ========================================================================
    
    def read_entity(self, entity_name: str) -> Optional[Dict[str, Any]]:
        """
        Read entity from Markdown, parse to structured data.
        
        Returns:
            {
                "metadata": {  # YAML frontmatter
                    "id": "nvidia",
                    "level": "L1",
                    "coordinates": [0.85, 0.0, 1.0, ...]
                },
                "content": "...",  # Markdown body
                "relations": ["tsmc", "ai_boom"],  # Parsed [[links]]
                "shadow_log": [...]  # Parsed shadow events
            }
        """
        path = self.entities_dir / f"{entity_name}.md"
        
        if not path.exists():
            return None
        
        if FRONTMATTER_AVAILABLE:
            # Parse Markdown with frontmatter
            post = frontmatter.load(path)
            metadata = post.metadata
            content = post.content
        else:
            # Fallback: manual parsing
            text = path.read_text()
            metadata = {}
            content = text
            
            # Simple YAML frontmatter parsing
            if text.startswith("---\n"):
                parts = text.split("---\n", 2)
                if len(parts) >= 3:
                    yaml_text = parts[1]
                    content = parts[2]
                    # Parse YAML manually (simple key: value)
                    for line in yaml_text.split("\n"):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            metadata[key.strip()] = value.strip()
        
        # Extract relations (wikilinks)
        relations = self._extract_wikilinks(content)
        
        # Parse shadow log
        shadow_log = self._extract_shadow_log(content)
        
        return {
            "metadata": metadata,
            "content": content,
            "relations": relations,
            "shadow_log": shadow_log,
            "path": str(path)
        }
    
    def _extract_wikilinks(self, content: str) -> List[str]:
        """Extract [[wikilinks]] from Markdown content."""
        pattern = r'\[\[([^\]]+)\]\]'
        return re.findall(pattern, content)
    
    def _extract_shadow_log(self, content: str) -> List[Dict[str, Any]]:
        """
        Parse shadow log from Markdown.
        
        Format:
        ### 2026-02-01 06:00 UTC
        Detected insider selling...
        **W-Axis Signal**: 0.8
        """
        logs = []
        
        # Find shadow log section
        if "## Shadow Log" in content:
            shadow_section = content.split("## Shadow Log")[1]
            
            # Find all ### entries
            entries = re.split(r'\n###\s+', shadow_section)
            
            for entry in entries[1:]:  # Skip first empty split
                lines = entry.strip().split("\n")
                if len(lines) < 2:
                    continue
                
                timestamp = lines[0].strip()
                description = "\n".join(lines[1:])
                
                # Extract W-Axis signal if present
                w_match = re.search(r'\*\*W-Axis Signal\*\*:\s*([-0-9.]+)', description)
                w_value = float(w_match.group(1)) if w_match else None
                
                logs.append({
                    "timestamp": timestamp,
                    "description": description,
                    "w_value": w_value
                })
        
        return logs
    
    def entity_to_manifold_point(self, entity_data: Dict[str, Any]) -> np.ndarray:
        """
        Convert entity metadata to 7D manifold coordinates.
        
        This is the bridge: Markdown → 6D Tensor
        """
        metadata = entity_data["metadata"]
        
        # If coordinates exist in frontmatter, use them
        if "coordinates" in metadata:
            coords = metadata["coordinates"]
            if isinstance(coords, str):
                # Parse string representation
                coords = json.loads(coords)
            return np.array(coords, dtype=float)
        
        # Otherwise, encode from semantic attributes
        level_str = metadata.get("level", "L3")
        if isinstance(level_str, str) and level_str.startswith("L"):
            level = int(level_str[1])
        else:
            level = 3
        
        domain = metadata.get("domain", "tech")
        
        stance_val = metadata.get("stance", 0.0)
        stance = float(stance_val) if isinstance(stance_val, (int, float, str)) else 0.0
        
        intent_val = metadata.get("intent", 0.0)
        intent = float(intent_val) if isinstance(intent_val, (int, float, str)) else 0.0
        
        time_val = metadata.get("time", 0.0)
        time = float(time_val) if isinstance(time_val, (int, float, str)) else 0.0
        
        scale_val = metadata.get("scale", 0.0)
        scale = float(scale_val) if isinstance(scale_val, (int, float, str)) else 0.0
        
        # Import manifold encoder
        try:
            from raywu_manifold_strict import RaywuManifold
            manifold = RaywuManifold()
            point = manifold.encode_agent_state(level, domain, stance, intent, time, scale)
            return point
        except ImportError:
            # Fallback: return dummy coordinates
            return np.array([level/5, 0, 1, 0, stance, intent, time])
    
    # ========================================================================
    # WRITE: Tensor → World (Incremental Update)
    # ========================================================================
    
    def update_entity(
        self,
        entity_name: str,
        updates: Dict[str, Any],
        log_entry: str,
        simulation_results: Optional[Dict[str, Any]] = None
    ):
        """
        核心写入逻辑：增量更新 (Incremental Update)
        
        NOT overwrite! This is the key difference from naive databases.
        
        Args:
            entity_name: e.g., "nvidia"
            updates: Metadata changes, e.g., {"stance": 0.9, "intent": -0.3}
            log_entry: Human-readable event description
            simulation_results: Results from manifold simulation
        """
        # 1. Read current state
        entity = self.read_entity(entity_name)
        
        if entity is None:
            # Create new entity
            entity = {
                "metadata": {
                    "id": entity_name,
                    "level": "L3",
                    "updated": self._timestamp()
                },
                "content": f"# Entity: {entity_name}\n\n## Current State\n\n"
            }
        
        # 2. Update metadata (State Transition)
        entity["metadata"].update(updates)
        entity["metadata"]["updated"] = self._timestamp()
        
        # 3. Append log (Event Log)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        new_log = f"\n\n### {timestamp}\n{log_entry}\n"
        
        if simulation_results:
            new_log += f"\n**Simulation Results:**\n```json\n{json.dumps(simulation_results, indent=2)}\n```\n"
        
        # Append to content
        if "## Timeline" not in entity["content"]:
            entity["content"] += "\n\n## Timeline\n"
        
        entity["content"] += new_log
        
        # 4. Write back to file
        path = self.entities_dir / f"{entity_name}.md"
        
        if FRONTMATTER_AVAILABLE:
            post = frontmatter.Post(
                entity["content"],
                **entity["metadata"]
            )
            with open(path, "wb") as f:
                frontmatter.dump(post, f)
        else:
            # Fallback: manual YAML + content
            yaml_lines = ["---"]
            for key, value in entity["metadata"].items():
                if isinstance(value, list):
                    yaml_lines.append(f"{key}: {json.dumps(value)}")
                else:
                    yaml_lines.append(f"{key}: {value}")
            yaml_lines.append("---\n")
            
            full_content = "\n".join(yaml_lines) + entity["content"]
            path.write_text(full_content)
        
        print(f"✓ Updated entity: {entity_name}")
    
    # ========================================================================
    # QUERY: Semantic Search (Vector + Text)
    # ========================================================================
    
    def query_world(
        self,
        query: str,
        max_results: int = 5,
        sources: List[str] = ["entities", "narratives"]
    ) -> List[Dict[str, Any]]:
        """
        Semantic search across world state.
        
        This would integrate with vector embeddings (like OpenClaw's memory search).
        
        Args:
            query: Natural language query
            max_results: Top-k results
            sources: Which directories to search
        
        Returns:
            List of matching entities/narratives with scores
        """
        results = []
        
        for source in sources:
            source_dir = self.root / source
            if not source_dir.exists():
                continue
            
            for md_file in source_dir.glob("*.md"):
                content = md_file.read_text()
                if query.lower() in content.lower():
                    # Simple text search (TODO: vector search)
                    results.append({
                        "path": str(md_file),
                        "name": md_file.stem,
                        "score": 0.8,  # Dummy score
                        "snippet": content[:200] + "..."
                    })
        
        return sorted(results, key=lambda x: x["score"], reverse=True)[:max_results]
    
    # ========================================================================
    # SNAPSHOT: Freeze World State for Simulation
    # ========================================================================
    
    def create_snapshot(self) -> Dict[str, Any]:
        """
        Create immutable snapshot of world state.
        
        This is what the manifold simulation operates on.
        Simulations never mutate the live world directly.
        """
        snapshot = {
            "timestamp": self._timestamp(),
            "entities": {},
            "relations": {},
            "narratives": {}
        }
        
        # Load all entities
        for entity_file in self.entities_dir.glob("*.md"):
            entity_name = entity_file.stem
            entity_data = self.read_entity(entity_name)
            if entity_data:
                snapshot["entities"][entity_name] = entity_data
        
        # Load relations
        for rel_file in self.relations_dir.glob("*.md"):
            rel_name = rel_file.stem
            snapshot["relations"][rel_name] = rel_file.read_text()
        
        # Load narratives
        for narr_file in self.narratives_dir.glob("*.md"):
            narr_name = narr_file.stem
            snapshot["narratives"][narr_name] = narr_file.read_text()
        
        print(f"✓ Snapshot created: {len(snapshot['entities'])} entities, {len(snapshot['relations'])} relations, {len(snapshot['narratives'])} narratives")
        
        return snapshot
    
    # ========================================================================
    # MEMORY: OpenClaw-style daily logs
    # ========================================================================
    
    def write_memory(self, content: str, date: Optional[str] = None):
        """
        Write to daily memory log (OpenClaw style).
        
        Args:
            content: Memory entry
            date: YYYY-MM-DD (defaults to today)
        """
        if date is None:
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        memory_file = self.memory_dir / f"{date}.md"
        
        # Append to daily log
        timestamp = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
        entry = f"\n### {timestamp}\n{content}\n"
        
        if memory_file.exists():
            existing = memory_file.read_text()
            memory_file.write_text(existing + entry)
        else:
            header = f"# Memory Log - {date}\n\n"
            memory_file.write_text(header + entry)
        
        print(f"✓ Memory written to: {date}.md")
    
    # ========================================================================
    # UTILS
    # ========================================================================
    
    def _timestamp(self) -> str:
        """ISO 8601 timestamp in UTC."""
        return datetime.now(timezone.utc).isoformat()
    
    def list_entities(self) -> List[str]:
        """List all entity names."""
        return [f.stem for f in self.entities_dir.glob("*.md")]
    
    def export_snapshot_json(self, output_path: str):
        """Export snapshot as JSON for backup/analysis."""
        snapshot = self.create_snapshot()
        
        with open(output_path, "w") as f:
            json.dump(snapshot, f, indent=2, default=str)
        
        print(f"✓ Snapshot exported to: {output_path}")


# ============================================================================
# Integration with Raywu Manifold
# ============================================================================

def integrate_world_and_manifold():
    """
    Example: How to connect World State ↔ Manifold Simulation
    """
    try:
        from raywu_manifold_strict import RaywuManifold
        MANIFOLD_AVAILABLE = True
    except ImportError:
        print("⚠️  Strict manifold not available")
        MANIFOLD_AVAILABLE = False
        return
    
    # 1. Initialize
    world = WorldStateManager(world_root="./world_state")
    manifold = RaywuManifold(warp_strength=100.0)
    
    print("\n" + "="*70)
    print("🔄 INTEGRATING WORLD STATE ↔ MANIFOLD SIMULATION")
    print("="*70 + "\n")
    
    # 2. READ: Load world state
    snapshot = world.create_snapshot()
    
    if len(snapshot["entities"]) == 0:
        print("⚠️  No entities in world state. Create some first.")
        return
    
    # 3. BUILD: Convert to manifold points
    agent_points = []
    agent_names = []
    
    for entity_name, entity_data in snapshot["entities"].items():
        point = world.entity_to_manifold_point(entity_data)
        agent_points.append(point)
        agent_names.append(entity_name)
    
    print(f"✓ Loaded {len(agent_names)} entities to manifold")
    
    # 4. SIMULATE: Run physics on manifold
    print("\n--- Computing Cognitive Distances ---\n")
    
    distances = []
    for i in range(len(agent_points)):
        for j in range(i+1, len(agent_points)):
            dist = manifold.cognitive_distance(agent_points[i], agent_points[j])
            distances.append((agent_names[i], agent_names[j], dist))
            print(f"  Distance({agent_names[i]} ↔ {agent_names[j]}): {dist:.4f}")
    
    # 5. COLLAPSE: Write results back to world
    print("\n--- Writing Simulation Results Back to World ---\n")
    
    for entity_name in agent_names:
        world.update_entity(
            entity_name,
            updates={"last_simulation": world._timestamp()},
            log_entry="Manifold simulation completed. Cognitive distances computed.",
            simulation_results={
                "status": "completed",
                "n_agents": len(agent_names),
                "distances": [
                    {
                        "to": pair[1] if pair[0] == entity_name else pair[0],
                        "distance": pair[2]
                    }
                    for pair in distances if entity_name in (pair[0], pair[1])
                ]
            }
        )
    
    print("\n" + "="*70)
    print("✅ World ↔ Manifold Integration Completed!")
    print("="*70)


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🌍 RAYWU WORLD STATE MANAGER - OpenClaw Style")
    print("="*70 + "\n")
    
    # Demo
    world = WorldStateManager()
    
    # Create sample entities
    print("Creating sample entities...\n")
    
    world.update_entity(
        "nvidia",
        updates={
            "level": "L1",
            "domain": "tech",
            "stance": 0.7,
            "intent": 0.8,
            "coordinates": [0.85, 0.0, 1.0, 0.0, 0.7, 0.8, 0.5]
        },
        log_entry="Initial state captured from market data. Stock price: $900. Bullish sentiment."
    )
    
    world.update_entity(
        "tsmc",
        updates={
            "level": "L1",
            "domain": "tech",
            "stance": 0.5,
            "intent": 0.6,
            "coordinates": [0.15, 0.0, 1.0, 0.0, 0.5, 0.6, 0.0]
        },
        log_entry="Semiconductor manufacturer. Key supplier to Nvidia. [[nvidia]]"
    )
    
    # Read back
    nvidia = world.read_entity("nvidia")
    print(f"\n✓ Entity 'nvidia' created:")
    print(f"  Metadata: {nvidia['metadata']}")
    print(f"  Relations: {nvidia['relations']}")
    
    # Update with simulation results
    world.update_entity(
        "nvidia",
        updates={"stance": 0.9},
        log_entry="Detected strong bullish signal from options flow. Large call buying at $950 strike.",
        simulation_results={
            "nash_equilibrium": [0.88, 0.0, 1.0, 0.0, 0.75, 0.85, 0.5],
            "consensus_strength": "STRONG",
            "dispersion": 0.12
        }
    )
    
    # Query world
    print("\n--- Querying World State ---\n")
    results = world.query_world("nvidia", max_results=3)
    for result in results:
        print(f"  Found: {result['name']} (score: {result['score']})")
    
    # Create snapshot
    print("\n--- Creating World Snapshot ---\n")
    snapshot = world.create_snapshot()
    
    # Write memory
    world.write_memory("Analyzed Nvidia stock. Bullish consensus emerging. Watch for potential overvaluation.")
    
    print("\n" + "="*70)
    print("✅ Demo Completed!")
    print("="*70)
    print("\nNext step: Run integrate_world_and_manifold() to connect with strict manifold.\n")
