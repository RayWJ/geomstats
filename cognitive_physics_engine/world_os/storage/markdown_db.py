"""
Markdown Database - World State Persistence Layer
==================================================

This module provides persistent storage for the WorldOS state using
Markdown files as the database.

Philosophy:
- Knowledge is dead info; World State is LIVING text
- Markdown is human-readable + LLM-friendly + Git-versionable
- Incremental updates (NOT overwrites) preserve history

Architecture:
/world_state/
  /entities/       # L1 Facts (companies, people, events)
  /relations/      # L3 Logic (supply chains, correlations)
  /narratives/     # L5 Strategy (AI boom, recession fear)
  /shadows/        # W Axis (hidden agendas, insider moves)
  /memory/         # Temporal snapshots (YYYY-MM-DD.md)

Author: Raywu WorldOS Team  
Date: 2026-02-01
Version: v61.0
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import numpy as np

# Optional: frontmatter for YAML parsing
try:
    import frontmatter
    FRONTMATTER_AVAILABLE = True
except ImportError:
    FRONTMATTER_AVAILABLE = False
    print("⚠️  python-frontmatter not available. Using fallback parser.")


class MarkdownDB:
    """
    File-based database using Markdown documents.
    
    Each entity/relation/narrative is stored as a .md file with:
    - YAML frontmatter (metadata)
    - Markdown body (narrative + logs)
    """
    
    def __init__(self, root_dir: str = "world_state"):
        """
        Initialize database.
        
        Args:
            root_dir: Root directory for world state files
        """
        self.root = Path(root_dir)
        self.entities_dir = self.root / "entities"
        self.relations_dir = self.root / "relations"
        self.narratives_dir = self.root / "narratives"
        self.shadows_dir = self.root / "shadows"
        self.memory_dir = self.root / "memory"
        
        # Create directories if they don't exist
        for dir_path in [self.entities_dir, self.relations_dir, 
                         self.narratives_dir, self.shadows_dir, self.memory_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def _parse_frontmatter(self, content: str) -> tuple[Dict[str, Any], str]:
        """Parse YAML frontmatter and body."""
        if FRONTMATTER_AVAILABLE:
            post = frontmatter.loads(content)
            return post.metadata, post.content
        else:
            # Fallback parser
            metadata = {}
            body = content
            
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    yaml_text = parts[1]
                    body = parts[2].strip()
                    
                    for line in yaml_text.strip().split("\n"):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            key = key.strip()
                            value = value.strip()
                            
                            # Try JSON parse for complex types
                            try:
                                value = json.loads(value)
                            except:
                                # Try numeric
                                try:
                                    if "." in value:
                                        value = float(value)
                                    else:
                                        value = int(value)
                                except:
                                    pass  # Keep as string
                            
                            metadata[key] = value
            
            return metadata, body
    
    def _serialize_frontmatter(self, metadata: Dict[str, Any], body: str) -> str:
        """Serialize metadata and body to Markdown."""
        if FRONTMATTER_AVAILABLE:
            post = frontmatter.Post(body, **metadata)
            return frontmatter.dumps(post)
        else:
            # Fallback serializer
            lines = ["---"]
            for key, value in metadata.items():
                if isinstance(value, (list, dict)):
                    value_str = json.dumps(value)
                else:
                    value_str = str(value)
                lines.append(f"{key}: {value_str}")
            lines.append("---")
            lines.append("")
            lines.append(body)
            return "\n".join(lines)
    
    def read_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """
        Read entity from database.
        
        Args:
            entity_id: Entity identifier (filename without .md)
        
        Returns:
            Dictionary with 'metadata' and 'body' keys, or None if not found
        """
        path = self.entities_dir / f"{entity_id}.md"
        
        if not path.exists():
            return None
        
        content = path.read_text(encoding="utf-8")
        metadata, body = self._parse_frontmatter(content)
        
        return {
            "id": entity_id,
            "metadata": metadata,
            "body": body,
            "path": str(path)
        }
    
    def write_entity(self, entity_id: str, metadata: Dict[str, Any], 
                     body: str, append_log: Optional[str] = None):
        """
        Write (or update) entity in database.
        
        Args:
            entity_id: Entity identifier
            metadata: YAML frontmatter dictionary
            body: Markdown body content
            append_log: Optional log entry to append
        """
        path = self.entities_dir / f"{entity_id}.md"
        
        # If appending to existing entity
        if append_log and path.exists():
            existing = self.read_entity(entity_id)
            if existing:
                # Merge metadata (new overwrites old)
                merged_metadata = {**existing['metadata'], **metadata}
                
                # Append to body
                timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                new_body = existing['body'] + f"\n\n## Update: {timestamp}\n{append_log}"
                
                content = self._serialize_frontmatter(merged_metadata, new_body)
                path.write_text(content, encoding="utf-8")
                return
        
        # Write new or overwrite
        content = self._serialize_frontmatter(metadata, body)
        path.write_text(content, encoding="utf-8")
    
    def update_entity(self, entity_id: str, updates: Dict[str, Any], 
                      log_message: str):
        """
        Incremental update (Git-style patch).
        
        Args:
            entity_id: Entity to update
            updates: Dictionary of fields to update in metadata
            log_message: Description of what changed
        """
        existing = self.read_entity(entity_id)
        
        if not existing:
            # Create new entity
            self.write_entity(entity_id, updates, "", log_message)
            return
        
        # Merge updates
        new_metadata = {**existing['metadata'], **updates}
        
        # Append log
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        log_entry = f"\n\n## Update: {timestamp}\n{log_message}"
        new_body = existing['body'] + log_entry
        
        # Write back
        content = self._serialize_frontmatter(new_metadata, new_body)
        path = self.entities_dir / f"{entity_id}.md"
        path.write_text(content, encoding="utf-8")
    
    def query_entities(self, filter_fn=None) -> List[Dict[str, Any]]:
        """
        Query all entities, optionally filtered.
        
        Args:
            filter_fn: Optional function(entity) -> bool
        
        Returns:
            List of entity dictionaries
        """
        results = []
        
        for path in self.entities_dir.glob("*.md"):
            entity_id = path.stem
            entity = self.read_entity(entity_id)
            
            if entity:
                if filter_fn is None or filter_fn(entity):
                    results.append(entity)
        
        return results
    
    def create_snapshot(self, description: str = "") -> str:
        """
        Create daily memory snapshot.
        
        Args:
            description: Optional description of the snapshot
        
        Returns:
            Path to snapshot file
        """
        today = datetime.utcnow().strftime("%Y-%m-%d")
        snapshot_path = self.memory_dir / f"{today}.md"
        
        # Gather statistics
        entity_count = len(list(self.entities_dir.glob("*.md")))
        relation_count = len(list(self.relations_dir.glob("*.md")))
        narrative_count = len(list(self.narratives_dir.glob("*.md")))
        
        # Build snapshot content
        lines = [
            f"# World State Snapshot: {today}",
            "",
            f"**Description**: {description or 'Daily snapshot'}",
            "",
            "## Statistics",
            f"- Entities: {entity_count}",
            f"- Relations: {relation_count}",
            f"- Narratives: {narrative_count}",
            "",
            "## Recent Updates",
            ""
        ]
        
        # List recent entities (last 5)
        entities = sorted(
            self.entities_dir.glob("*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )[:5]
        
        for entity_path in entities:
            entity = self.read_entity(entity_path.stem)
            if entity:
                level = entity['metadata'].get('level', 'N/A')
                domain = entity['metadata'].get('domain', 'N/A')
                lines.append(f"- **{entity['id']}** (Level: {level}, Domain: {domain})")
        
        content = "\n".join(lines)
        snapshot_path.write_text(content, encoding="utf-8")
        
        return str(snapshot_path)


# ============================================================================
# DEMO
# ============================================================================

def demo_markdown_db():
    """Demonstrate Markdown database operations."""
    print("\n" + "="*70)
    print("📚 MARKDOWN DATABASE DEMO")
    print("="*70 + "\n")
    
    # Initialize DB
    db = MarkdownDB(root_dir="demo_world_state")
    print("✓ Database initialized at: demo_world_state/")
    print()
    
    # Write entity
    print("📝 Writing entity: NVIDIA")
    db.write_entity(
        entity_id="nvidia",
        metadata={
            "level": "L1",
            "domain": "tech",
            "stance": 0.7,
            "intent": 0.8,
            "coordinates": [0.85, 0.0, 1.0, 0.0, 0.7, 0.8, 0.5]
        },
        body="""# Entity: NVIDIA

## Current State
Stock price: $900
Sentiment: Bullish

## Timeline
- 2024-05-01: Initial state captured
"""
    )
    print("✓ Entity written")
    print()
    
    # Update entity
    print("📝 Updating entity: NVIDIA")
    db.update_entity(
        entity_id="nvidia",
        updates={"stance": 0.9},
        log_message="Strong bullish signal from options flow. Large call buying at $950 strike."
    )
    print("✓ Entity updated (incremental)")
    print()
    
    # Read entity
    print("📖 Reading entity: NVIDIA")
    nvidia = db.read_entity("nvidia")
    print(f"  Metadata: {nvidia['metadata']}")
    print(f"  Body (first 100 chars): {nvidia['body'][:100]}...")
    print()
    
    # Query entities
    print("🔍 Query entities (tech domain)")
    tech_entities = db.query_entities(
        filter_fn=lambda e: e['metadata'].get('domain') == 'tech'
    )
    print(f"  Found {len(tech_entities)} tech entities:")
    for entity in tech_entities:
        print(f"    - {entity['id']}")
    print()
    
    # Create snapshot
    print("📸 Creating snapshot")
    snapshot_path = db.create_snapshot("Demo snapshot after NVIDIA update")
    print(f"  Snapshot saved: {snapshot_path}")
    print()
    
    print("="*70)
    print("✅ Markdown DB demo completed!")
    print("="*70)


if __name__ == "__main__":
    demo_markdown_db()
