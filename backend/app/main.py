from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import os
from dotenv import load_dotenv

from .database import engine, Base
from .api.endpoints import router as api_router

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Resume-Job Description Matcher API",
    description="AI-powered tool to match resumes with job descriptions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

# Serve static files (for frontend)
if os.path.exists("../frontend"):
    app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Serve the frontend index page
    """
    try:
        frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend/index.html")
        if os.path.exists(frontend_path):
            with open(frontend_path, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        else:
            return HTMLResponse(content="""
            <html>
                <head>
                    <title>Resume-Job Description Matcher</title>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                </head>
                <body class="bg-light">
                    <div class="container mt-5">
                        <div class="row justify-content-center">
                            <div class="col-md-8">
                                <div class="card shadow">
                                    <div class="card-body text-center">
                                        <h1 class="card-title text-primary mb-4">
                                            Resume-Job Description Matcher
                                        </h1>
                                        <p class="lead">
                                            AI-powered tool to analyze how well your resume matches job descriptions
                                        </p>
                                        <div class="alert alert-info">
                                            <strong>API Documentation:</strong> 
                                            <a href="/docs">Swagger Docs</a> | 
                                            <a href="/redoc">ReDoc</a>
                                        </div>
                                        <p class="text-muted">
                                            Frontend is being served from the /static endpoint
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
            """)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading frontend</h1><p>{str(e)}</p>")

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "Resume-Job Description Matcher",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": "1.0.0"
    }

# Application startup and shutdown events
@app.on_event("startup")
async def startup_event():
    print("🚀 Resume-Job Description Matcher API started successfully")
    print("📚 API Documentation available at: /docs")
    print("🔍 Alternative docs at: /redoc")

@app.on_event("shutdown")
async def shutdown_event():
    print("👋 Resume-Job Description Matcher API shutting down")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT", "development") == "development"
    )
