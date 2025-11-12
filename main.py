from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
from datetime import datetime
from typing import Any

# async batch processing
from services.async_pipeline import process_bulk_async

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Recruitment Enhancement Microservice",
    description="Intelligent layer for ATS platforms providing JD optimization, candidate scoring, skill gap analysis, and bias detection",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    services: Dict[str, str]

class JDOptimizationRequest(BaseModel):
    job_title: str
    department: str
    raw_description: str
    responsibilities: List[str]
    required_skills: List[str]
    company_name: Optional[str] = "Your Company"
    tone: Optional[str] = "professional"

class JDOptimizationResponse(BaseModel):
    optimized_jd: Dict
    analysis: Dict
    recommendations: List[str]

class CandidateScoringRequest(BaseModel):
    resume_text: str
    job_description: str
    required_skills: List[str]
    required_experience_years: Optional[int] = 0

class CandidateScoringResponse(BaseModel):
    candidate_id: str
    overall_score: float
    components: Dict[str, float]
    explanation: Dict

# Routes
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "AI-Powered Recruitment Enhancement Microservice",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        services={
            "api": "running",
            "database": "not_configured",
            "ml_models": "not_loaded"
        }
    )

@app.post("/api/v1/jd/optimize", response_model=JDOptimizationResponse)
async def optimize_job_description(request: JDOptimizationRequest):
    """
    Optimize a job description using AI
    
    This endpoint generates an optimized job description with:
    - Enhanced clarity and structure
    - Bias-free language
    - SEO optimization
    - Inclusivity improvements
    """
    # Mock response for demo
    return JDOptimizationResponse(
        optimized_jd={
            "title": f"{request.job_title} - {request.company_name}",
            "summary": f"Join {request.company_name}'s {request.department} team as a {request.job_title}. We're looking for a talented professional to contribute to our mission.",
            "responsibilities": request.responsibilities,
            "requirements": request.required_skills,
            "company_culture": "We value diversity, innovation, and collaboration."
        },
        analysis={
            "readability_score": 75.5,
            "inclusivity_score": 92,
            "seo_score": 85,
            "bias_indicators": {
                "gender_coded_words": [],
                "exclusionary_jargon": [],
                "overall_inclusivity": 92
            }
        },
        recommendations=[
            "Great inclusivity! Consider adding salary range for transparency.",
            "SEO: Strong keyword usage. Add location keywords for better local search.",
            "Structure: Well-organized. Consider adding 'What We Offer' section."
        ]
    )

@app.post("/api/v1/candidates/score", response_model=CandidateScoringResponse)
async def score_candidate(request: CandidateScoringRequest):
    """
    Score and rank a candidate against job requirements
    
    Uses semantic matching and NLP to provide:
    - Overall match score (0-100)
    - Component breakdowns (skills, experience, education)
    - Explainable AI reasoning
    """
    # Mock response for demo
    import hashlib
    candidate_id = hashlib.md5(request.resume_text.encode()).hexdigest()[:12]
    
    return CandidateScoringResponse(
        candidate_id=candidate_id,
        overall_score=87.5,
        components={
            "skills": 92.0,
            "experience": 85.0,
            "education": 100.0,
            "semantic_similarity": 78.0
        },
        explanation={
            "strengths": [
                f"Strong match on required skills: {', '.join(request.required_skills[:3])}",
                "Exceeds experience requirement" if request.required_experience_years > 0 else "Relevant experience demonstrated"
            ],
            "gaps": [
                "Consider additional training in advanced topics"
            ],
            "recommendation": "STRONG FIT - Highly recommended for interview"
        }
    )


@app.post("/api/v1/candidates/score/batch")
async def score_candidates_batch(requests: List[Dict[str, Any]]):
    """Process 10-20 resumes efficiently in parallel and return ranked results.

    Accepts a JSON array of objects with:
    - resume_text (str)
    - job_description (str)
    - required_skills (List[str])
    - fileName (optional str) - preserved in results
    """
    items = []
    for r in requests:
        items.append({
            "resume_text": r.get("resume_text", ""),
            "job_description": r.get("job_description", ""),
            "required_skills": r.get("required_skills", []),
            "fileName": r.get("fileName", "Unknown"),  # Preserve fileName from frontend
        })

    try:
        results = await process_bulk_async(items)
        return results
    except Exception as e:
        import traceback
        print(f"[ERROR] Batch endpoint failed: {str(e)}")
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Batch processing failed: {str(e)}")

@app.post("/api/v1/bias/analyze")
async def analyze_bias(
    candidates: List[Dict],
    scoring_results: List[Dict],
    threshold_score: float = 70.0
):
    """
    Analyze hiring process for bias and disparate impact
    
    Checks for:
    - Disparate impact (Four-Fifths Rule)
    - Proxy variable detection
    - Statistical significance of disparities
    """
    # Mock response for demo
    return {
        "overall_compliance": True,
        "violations": [],
        "metrics": {
            "gender": {
                "compliant": True,
                "selection_rates": {
                    "male": 0.75,
                    "female": 0.72
                },
                "impact_ratio": 0.96
            }
        },
        "recommendations": [
            "No disparate impact detected. Continue monitoring.",
            "Maintain diverse candidate pipeline."
        ]
    }

@app.get("/api/v1/integrations/status")
async def integration_status():
    """Check status of ATS integrations"""
    return {
        "integrations": [
            {
                "name": "Greenhouse",
                "status": "configured",
                "health": "not_tested"
            },
            {
                "name": "Lever",
                "status": "not_configured",
                "health": "not_tested"
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
