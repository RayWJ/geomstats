"""
WorldOS API Server - FastAPI Backend
=====================================

This server provides REST API endpoints for WorldOS v61.0,
connecting the frontend to the new cognitive physics engine.

Endpoints:
- POST /api/entity/create - Create new entity
- GET  /api/entity/{id} - Get entity state
- POST /api/entity/{id}/tick - Execute simulation tick
- POST /api/entity/{id}/episode - Run episode
- GET  /api/world/snapshot - Get world state snapshot
- POST /api/llm/analyze - LLM trajectory analysis
- GET  /api/manifold/info - Get manifold information
- GET  /api/visualization/data - Get visualization data

Author: Raywu WorldOS Team
Date: 2026-02-01
Version: v61.0
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import sys
import os
from pathlib import Path
import json
import numpy as np

# Add world_os to path
world_os_path = Path(__file__).parent
sys.path.insert(0, str(world_os_path / "kernel"))
sys.path.insert(0, str(world_os_path / "brain"))
sys.path.insert(0, str(world_os_path / "storage"))

from manifold import CognitiveManifold
from dynamics import PhysicsEngine, PotentialField
from translator import NeuroSymbolicTranslator
from markdown_db import MarkdownDB
from llm_agent import LLMAgent
from engine import WorldOS


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class EntityMetadata(BaseModel):
    level: int = Field(3, ge=1, le=5, description="Cognitive level (1-5)")
    domain: str = Field("tech", description="Domain (tech, finance, etc.)")
    stance: float = Field(0.0, ge=-1.0, le=1.0, description="Stance (-1 to 1)")
    intent: float = Field(0.0, ge=-1.0, le=1.0, description="Intent (-1 to 1)")
    time: float = Field(0.0, ge=-1.0, le=1.0, description="Time focus")
    scale: float = Field(0.0, ge=-1.0, le=1.0, description="Scale")


class EntityCreateRequest(BaseModel):
    entity_id: str = Field(..., description="Unique entity identifier")
    metadata: EntityMetadata = Field(..., description="Entity metadata")
    description: str = Field("", description="Entity description")


class TickRequest(BaseModel):
    llm_intervention: bool = Field(False, description="Use LLM for this tick")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class EpisodeRequest(BaseModel):
    num_ticks: int = Field(5, ge=1, le=100, description="Number of ticks")
    llm_frequency: int = Field(3, ge=1, le=10, description="LLM every N ticks")


class LLMAnalysisRequest(BaseModel):
    initial_state: Dict[str, Any]
    final_state: Dict[str, Any]
    trajectory_stats: Dict[str, float]
    entity_context: str = ""


class EntityResponse(BaseModel):
    entity_id: str
    metadata: Dict[str, Any]
    body: str
    coordinates: List[float]


class TickResponse(BaseModel):
    status: str
    tick: int
    entity_id: str
    distance: float
    decoded: Dict[str, Any]
    intervention: bool
    llm_decision: Optional[str]
    elapsed_time: float


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="WorldOS API",
    description="REST API for Raywu Cognitive Physics Engine v61.0",
    version="61.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global WorldOS instance
world_os = None

# Mount frontend static files
frontend_dir = Path(__file__).parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")


@app.on_event("startup")
async def startup_event():
    """Initialize WorldOS on startup."""
    global world_os
    
    print("\n" + "="*70)
    print("🌍 WORLDOS API SERVER STARTING")
    print("="*70 + "\n")
    
    # Initialize WorldOS
    world_os = WorldOS(
        world_state_dir="api_world_state",
        tick_duration=1.0,
        gamma=0.3,
        sigma=0.05,
        llm_model="gpt-4"
    )
    
    print("\n✅ API Server Ready!")
    print("="*70 + "\n")


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Serve frontend."""
    frontend_file = Path(__file__).parent / "frontend" / "index.html"
    if frontend_file.exists():
        return FileResponse(frontend_file)
    
    return {
        "name": "WorldOS API",
        "version": "61.0",
        "description": "Cognitive Physics Engine with Riemannian manifold simulation",
        "endpoints": {
            "entity": "/api/entity/*",
            "world": "/api/world/*",
            "llm": "/api/llm/*",
            "manifold": "/api/manifold/*",
            "visualization": "/api/visualization/*"
        }
    }


@app.get("/api")
async def api_root():
    """API documentation."""
    return {
        "name": "WorldOS API",
        "version": "61.0",
        "endpoints": {
            "entity": "/api/entity/*",
            "world": "/api/world/*",
            "llm": "/api/llm/*",
            "manifold": "/api/manifold/*",
            "visualization": "/api/visualization/*"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "worldos_initialized": world_os is not None,
        "llm_available": world_os.llm.available if world_os else False
    }


# ----------------------------------------------------------------------------
# ENTITY ENDPOINTS
# ----------------------------------------------------------------------------

@app.post("/api/entity/create", response_model=EntityResponse)
async def create_entity(request: EntityCreateRequest):
    """Create a new entity in the world state."""
    try:
        from datetime import datetime
        meta = request.metadata
        
        # Create metadata dict
        metadata = {
            "level": f"L{meta.level}",
            "domain": meta.domain,
            "stance": meta.stance,
            "intent": meta.intent,
            "time": meta.time,
            "scale": meta.scale
        }
        
        # Encode to get coordinates
        point = world_os.manifold.encode_state(
            level=meta.level,
            domain=meta.domain,
            stance=meta.stance,
            intent=meta.intent,
            time=meta.time,
            scale=meta.scale
        )
        
        metadata["coordinates"] = point.tolist()
        
        # Create body
        body = f"""# Entity: {request.entity_id}

{request.description}

## Properties
- Level: {metadata['level']}
- Domain: {metadata['domain']}
- Stance: {metadata['stance']}
- Intent: {metadata['intent']}
- Time: {metadata['time']}
- Scale: {metadata['scale']}

## Coordinates
{metadata['coordinates']}

Created via API at {datetime.now().isoformat()}.
"""
        
        # Write to database
        world_os.db.write_entity(
            entity_id=request.entity_id,
            metadata=metadata,
            body=body
        )
        
        return EntityResponse(
            entity_id=request.entity_id,
            metadata=metadata,
            body=body,
            coordinates=point.tolist()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/entity/list")
async def list_entities():
    """List all entities."""
    entities = world_os.db.query_entities()
    
    return {
        "count": len(entities),
        "entities": [
            {
                "id": e["id"],
                "level": e["metadata"].get("level"),
                "domain": e["metadata"].get("domain"),
                "stance": e["metadata"].get("stance")
            }
            for e in entities
        ]
    }


@app.get("/api/entity/{entity_id}", response_model=EntityResponse)
async def get_entity(entity_id: str):
    """Get entity state."""
    entity = world_os.db.read_entity(entity_id)
    
    if not entity:
        raise HTTPException(status_code=404, detail=f"Entity '{entity_id}' not found")
    
    return EntityResponse(
        entity_id=entity_id,
        metadata=entity["metadata"],
        body=entity["body"],
        coordinates=entity["metadata"].get("coordinates", [])
    )


@app.post("/api/entity/{entity_id}/tick", response_model=TickResponse)
async def execute_tick(entity_id: str, request: TickRequest):
    """Execute one simulation tick for entity."""
    try:
        result = world_os.tick(
            entity_id=entity_id,
            context=request.context,
            llm_intervention=request.llm_intervention
        )
        
        return TickResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/entity/{entity_id}/episode")
async def run_episode(entity_id: str, request: EpisodeRequest):
    """Run episode (multiple ticks)."""
    try:
        results = world_os.run_episode(
            entity_id=entity_id,
            num_ticks=request.num_ticks,
            llm_frequency=request.llm_frequency
        )
        
        # Convert numpy arrays to lists
        json_results = []
        for r in results:
            r_copy = r.copy()
            if "decoded" in r_copy and "coordinates" in r_copy["decoded"]:
                coords = r_copy["decoded"]["coordinates"]
                if hasattr(coords, 'tolist'):
                    r_copy["decoded"]["coordinates"] = coords.tolist()
            json_results.append(r_copy)
        
        return {
            "status": "success",
            "entity_id": entity_id,
            "total_ticks": len(json_results),
            "total_distance": sum(r["distance"] for r in json_results),
            "interventions": sum(1 for r in json_results if r["intervention"]),
            "results": json_results
        }
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



# ----------------------------------------------------------------------------
# WORLD ENDPOINTS
# ----------------------------------------------------------------------------

@app.get("/api/world/snapshot")
async def get_snapshot():
    """Get world state snapshot."""
    snapshot_path = world_os.db.create_snapshot("API snapshot request")
    
    # Read snapshot content
    with open(snapshot_path, 'r') as f:
        content = f.read()
    
    return {
        "status": "success",
        "snapshot_path": snapshot_path,
        "content": content
    }


@app.get("/api/world/stats")
async def get_world_stats():
    """Get world statistics."""
    entities = world_os.db.query_entities()
    
    # Compute statistics
    levels = {}
    domains = {}
    
    for entity in entities:
        level = entity["metadata"].get("level", "N/A")
        domain = entity["metadata"].get("domain", "N/A")
        
        levels[level] = levels.get(level, 0) + 1
        domains[domain] = domains.get(domain, 0) + 1
    
    return {
        "total_entities": len(entities),
        "by_level": levels,
        "by_domain": domains,
        "tick_count": world_os.tick_count
    }


# ----------------------------------------------------------------------------
# LLM ENDPOINTS
# ----------------------------------------------------------------------------

@app.post("/api/llm/analyze")
async def llm_analyze(request: LLMAnalysisRequest):
    """Use LLM to analyze trajectory."""
    try:
        analysis = world_os.llm.analyze_trajectory(
            initial_state=request.initial_state,
            final_state=request.final_state,
            trajectory_stats=request.trajectory_stats,
            entity_context=request.entity_context
        )
        
        return analysis
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/llm/intervention")
async def llm_intervention(analysis: Dict[str, Any]):
    """Get LLM intervention decision."""
    try:
        decision = world_os.llm.decide_intervention(analysis)
        return decision
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/llm/narrative")
async def llm_narrative(
    trajectory_analysis: Dict[str, Any],
    entity_name: str
):
    """Generate narrative from trajectory."""
    try:
        narrative = world_os.llm.generate_narrative(
            trajectory_analysis=trajectory_analysis,
            entity_name=entity_name
        )
        
        return {"narrative": narrative}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------------------------------------------
# MANIFOLD ENDPOINTS
# ----------------------------------------------------------------------------

@app.get("/api/manifold/info")
async def get_manifold_info():
    """Get manifold information."""
    return {
        "structure": "H³ × S² × R⁴",
        "embedding_dim": 10,
        "intrinsic_dim": 9,
        "components": {
            "hyperbolic": {
                "dim": 3,
                "description": "Hierarchical levels (L5-L1)"
            },
            "sphere": {
                "dim": 3,
                "description": "Domain topology (embedded S² in R³)"
            },
            "euclidean": {
                "dim": 4,
                "description": "Stance, Intent, Time, Scale"
            }
        },
        "physics": {
            "gamma": world_os.physics.gamma,
            "sigma": world_os.physics.sigma
        }
    }


@app.post("/api/manifold/distance")
async def compute_distance(point_a: List[float], point_b: List[float]):
    """Compute cognitive distance between two points."""
    try:
        point_a = np.array(point_a)
        point_b = np.array(point_b)
        
        distance = world_os.manifold.metric.dist(point_a, point_b)
        
        return {
            "distance": float(distance),
            "point_a": point_a.tolist(),
            "point_b": point_b.tolist()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------------------------------------------
# VISUALIZATION ENDPOINTS
# ----------------------------------------------------------------------------

@app.get("/api/visualization/data")
async def get_visualization_data():
    """Get visualization data for frontend."""
    entities = world_os.db.query_entities()
    
    viz_data = {
        "entities": [],
        "manifold": {
            "structure": "H³ × S² × R⁴",
            "embedding_dim": 10
        }
    }
    
    for entity in entities:
        coords = entity["metadata"].get("coordinates", [])
        decoded = world_os.manifold.decode_state(np.array(coords)) if coords else {}
        
        viz_data["entities"].append({
            "id": entity["id"],
            "coordinates": coords,
            "level": entity["metadata"].get("level"),
            "domain": entity["metadata"].get("domain"),
            "stance": decoded.get("stance", "unknown"),
            "intent": decoded.get("intent", "unknown")
        })
    
    return viz_data


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "worldos_api:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
