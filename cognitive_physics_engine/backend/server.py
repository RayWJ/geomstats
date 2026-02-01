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


if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
