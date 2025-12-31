"""
Main Application Entry Point

This file initializes and configures the FastAPI application.
It's the "glue" that brings everything together.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import issues

# Create database tables
# Base.metadata.create_all() creates tables based on our models
# This runs when the app starts and creates tables if they don't exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Issue Tracker API",
    description="A simple REST API for tracking and managing issues",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI at /docs
    redoc_url="/redoc"  # ReDoc documentation at /redoc
)

# CORS Middleware Configuration
# CORS = Cross-Origin Resource Sharing
# Allows frontend apps from different domains to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include routers
# This registers all the routes from our issues router
app.include_router(issues.router)


@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint - basic health check.
    
    Returns API information and available endpoints.
    Useful for:
    - Checking if the API is running
    - Quick reference for developers
    - Load balancer health checks
    """
    return {
        "message": "Welcome to Issue Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "create_issue": "POST /issues/",
            "list_issues": "GET /issues/",
            "get_issue": "GET /issues/{id}",
            "update_issue": "PUT /issues/{id}",
            "partial_update": "PATCH /issues/{id}",
            "delete_issue": "DELETE /issues/{id}"
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    
    Used by:
    - Monitoring systems (Prometheus, Datadog, etc.)
    - Load balancers to check if instance is healthy
    - Container orchestration (Kubernetes health probes)
    
    Returns simple status to confirm API is responsive.
    """
    return {"status": "healthy"}


# This allows running the app directly with: python -m app.main
# Usually we use uvicorn command instead, but this is helpful for debugging
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)