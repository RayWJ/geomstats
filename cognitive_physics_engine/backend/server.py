"""
FastAPI Backend Server for Cognitive Physics Engine

Provides REST API endpoints for:
- Querying the world simulator
- Injecting new information
- Comparing scenarios
- Retrieving simulation trajectories
- 3D visualization data
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import sys
import os

# Add cpe to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cpe'))

from cpe import WorldSimulator


# Pydantic models for API
class QueryRequest(BaseModel):
    question: str = Field(..., description="The question to ask")
    n_viewpoints: int = Field(100, ge=10, le=1000, description="Number of viewpoints")
    diversity: float = Field(0.3, ge=0.1, le=1.0, description="Diversity of viewpoints")
    simulation_time: float = Field(10.0, ge=1.0, le=60.0, description="Simulation time")
    dt: float = Field(0.1, ge=0.01, le=1.0, description="Integration time step")
    method: str = Field("euler", description="Integration method (euler or rk4)")
    return_details: bool = Field(False, description="Return detailed trajectory data")


class InjectRequest(BaseModel):
    information: str = Field(..., description="New information to inject")


class ScenarioComparisonRequest(BaseModel):
    question: str = Field(..., description="Base question")
    scenarios: List[str] = Field(..., description="List of scenario descriptions")
    n_viewpoints: int = Field(80, ge=10, le=1000)
    simulation_time: float = Field(5.0, ge=1.0, le=60.0)


class QueryResponse(BaseModel):
    question: str
    consensus: str
    confidence: float
    n_clusters: int
    n_viewpoints: int
    simulation_time: float
    details: Optional[Dict[str, Any]] = None


# Initialize FastAPI app
app = FastAPI(
    title="Cognitive Physics Engine API",
    description="REST API for the World Simulator - Computing truth in curved space",
    version="0.1.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global simulator instance
simulator = None


@app.on_event("startup")
async def startup_event():
    """Initialize the world simulator on startup."""
    global simulator
    print("\n🚀 Starting Cognitive Physics Engine API...")
    
    simulator = WorldSimulator(
        backend='numpy',
        hidden_dim=128,
        n_layers=3,
        friction=0.1
    )
    
    print("✓ API Ready!\n")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Cognitive Physics Engine API",
        "version": "0.1.0",
        "description": "A prototype 'World Simulator' that computes truth in curved space",
        "endpoints": {
            "/query": "POST - Query the simulator",
            "/inject": "POST - Inject new information",
            "/compare": "POST - Compare scenarios",
            "/health": "GET - Health check",
            "/docs": "GET - API documentation"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "simulator_initialized": simulator is not None
    }


@app.post("/query", response_model=QueryResponse)
async def query_simulator(request: QueryRequest):
    """
    Query the world simulator with a question.
    
    The simulator will:
    1. Generate diverse viewpoints
    2. Simulate collapse on the cognitive manifold
    3. Identify equilibrium clusters
    4. Synthesize a consensus answer
    """
    if simulator is None:
        raise HTTPException(status_code=503, detail="Simulator not initialized")
    
    try:
        result = simulator.query(
            question=request.question,
            n_viewpoints=request.n_viewpoints,
            diversity=request.diversity,
            simulation_time=request.simulation_time,
            dt=request.dt,
            method=request.method,
            return_details=request.return_details
        )
        
        return QueryResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")


@app.post("/inject")
async def inject_information(request: InjectRequest):
    """
    Inject new information to modify the potential field.
    
    This simulates "breaking news" that changes the cognitive landscape.
    """
    if simulator is None:
        raise HTTPException(status_code=503, detail="Simulator not initialized")
    
    try:
        simulator.inject_information(request.information)
        
        return {
            "status": "success",
            "message": f"Injected information: {request.information[:100]}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Injection error: {str(e)}")


@app.post("/compare")
async def compare_scenarios(request: ScenarioComparisonRequest):
    """
    Compare multiple scenarios for the same question.
    
    Returns consensus for each scenario to see how new information
    changes the outcome.
    """
    if simulator is None:
        raise HTTPException(status_code=503, detail="Simulator not initialized")
    
    try:
        results = simulator.compare_scenarios(
            question=request.question,
            scenarios=request.scenarios,
            n_viewpoints=request.n_viewpoints,
            simulation_time=request.simulation_time
        )
        
        return {
            "question": request.question,
            "n_scenarios": len(request.scenarios),
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison error: {str(e)}")


@app.get("/manifold/info")
async def manifold_info():
    """Get information about the cognitive manifold structure."""
    if simulator is None:
        raise HTTPException(status_code=503, detail="Simulator not initialized")
    
    return {
        "dimensions": simulator.manifold.dim_names,
        "structure": {
            "spatial": {
                "type": "Hyperbolic",
                "dims": ["Z_Level", "Y_Domain", "X_Stance"],
                "description": "3D hyperbolic space for hierarchical cognitive structure"
            },
            "evolution": {
                "type": "Euclidean",
                "dims": ["W_Intent", "T_Time", "S_Scale"],
                "description": "3D Euclidean space for linear evolution"
            }
        }
    }


@app.get("/examples")
async def get_examples():
    """Get example queries to try."""
    return {
        "examples": [
            {
                "question": "What is the outlook for NVIDIA stock?",
                "description": "Financial sentiment analysis"
            },
            {
                "question": "Should we invest in AI infrastructure?",
                "description": "Strategic investment decision"
            },
            {
                "question": "Is quantum computing ready for production?",
                "description": "Technology readiness assessment"
            },
            {
                "question": "What are the risks of climate change?",
                "description": "Risk analysis with multiple perspectives"
            }
        ]
    }


# ==================== VISUALIZATION ENDPOINTS ====================

@app.get("/visualization/data")
async def get_visualization_data():
    """Get complete visualization data for manifold rendering."""
    try:
        from cpe.manifold_visualizer import ManifoldVisualizer
        from cpe.raywu_manifold import RaywuCognitiveManifold
        from cpe.deep_state_agent_geometric import DeepStateEngineGeometric, Agent, AgentRole
        
        # Initialize
        manifold = RaywuCognitiveManifold()
        visualizer = ManifoldVisualizer(manifold)
        
        # Create sample agents
        engine = DeepStateEngineGeometric(manifold)
        agents = engine.initialize_agents_from_question(
            "What is the future of AI?",
            domains=["tech", "finance", "ethics"]
        )
        
        # Generate visualization data
        viz_data = visualizer.generate_complete_visualization(agents)
        
        return viz_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visualization error: {str(e)}")


@app.post("/visualization/agents")
async def visualize_custom_agents(request: QueryRequest):
    """Generate visualization data for a custom query."""
    try:
        from cpe.manifold_visualizer import ManifoldVisualizer
        from cpe.raywu_manifold import RaywuCognitiveManifold
        from cpe.deep_state_agent_geometric import DeepStateEngineGeometric
        
        # Initialize
        manifold = RaywuCognitiveManifold()
        visualizer = ManifoldVisualizer(manifold)
        
        # Run simulation
        engine = DeepStateEngineGeometric(manifold)
        agents = engine.initialize_agents_from_question(
            request.question,
            domains=["tech", "finance", "politics"]
        )
        
        # Run a few loops to get dynamics
        engine.run_agent_loop(max_loops=5)
        
        # Generate visualization
        viz_data = visualizer.generate_complete_visualization(engine.agents)
        viz_data["question"] = request.question
        viz_data["loops"] = engine.loop_count
        
        return viz_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visualization error: {str(e)}")


@app.get("/visualization/geodesic")
async def compute_geodesic_visualization(
    level1: int = 1,
    domain1: str = "tech",
    stance1: float = 0.8,
    level2: int = 5,
    domain2: str = "finance",
    stance2: float = -0.8
):
    """Compute and visualize a geodesic between two points."""
    try:
        from cpe.manifold_visualizer import ManifoldVisualizer
        from cpe.raywu_manifold import RaywuCognitiveManifold
        
        manifold = RaywuCognitiveManifold()
        visualizer = ManifoldVisualizer(manifold)
        
        # Encode two points
        point1 = manifold.encode_agent_state(level1, domain1, stance1, 0.5, 0.0, 0.0)
        point2 = manifold.encode_agent_state(level2, domain2, stance2, -0.5, 0.0, 0.0)
        
        # Compute geodesic
        geodesic_points = visualizer.compute_geodesic(point1, point2, n_steps=50)
        
        # Project to Poincaré disk
        poincare_geodesic = []
        for pt in geodesic_points:
            disk_pt = visualizer.project_to_poincare_disk(pt[:2])[0]
            poincare_geodesic.append(disk_pt.tolist())
        
        # Compute distance
        distance = manifold.cognitive_distance(point1, point2)
        
        return {
            "geodesic": poincare_geodesic,
            "distance": float(distance),
            "point1": {
                "level": level1,
                "domain": domain1,
                "stance": stance1
            },
            "point2": {
                "level": level2,
                "domain": domain2,
                "stance": stance2
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Geodesic error: {str(e)}")


if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
