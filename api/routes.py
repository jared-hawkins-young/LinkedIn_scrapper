import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from scraper import scrape_linkedin_profile


# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

class ScrapeRequest(BaseModel):
    linkedin_url: str  # LinkedIn profile URL


@router.get("/")
async def health_check():
    """Health check endpoint."""
    logger.info("Health check requested.")
    return {"status": "healthy"}

@router.post("/scrape")
async def scrape_profile(request: ScrapeRequest):
    """API endpoint to scrape a LinkedIn profile."""

    logger.info(f"Received request to scrape: {request.linkedin_url}")

    scraped_data = scrape_linkedin_profile(request.linkedin_url)
    
    if "error" in scraped_data:
        raise HTTPException(status_code=500, detail=scraped_data["error"])

    return scraped_data