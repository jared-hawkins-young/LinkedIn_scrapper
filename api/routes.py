import logging
from fastapi import APIRouter, File, HTTPException, UploadFile, Depends, Header
from flask import jsonify
from pydantic import BaseModel
from requests import request
from scraper import scrape_linkedin_profile
from scraper_html import scrape_linkedin_html


# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

SECRET_API_KEY = "b7f4a2c8d9e1f03b5c6d7a8e9f0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b"

class ScrapeRequest(BaseModel):
    linkedin_url: str  # LinkedIn profile URL

class ScrapeHTMLRequest(BaseModel):
    html_content: str 

def verify_api_key(x_api_key: str = Header(None)):
    """Middleware function to verify API key"""
    if x_api_key != SECRET_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@router.get("/")
async def health_check():
    """Health check endpoint."""
    logger.info("Health check requested.")
    return {"status": "healthy"}

@router.post("/scrape", dependencies=[Depends(verify_api_key)])
async def scrape_profile(request: ScrapeRequest):
    """API endpoint to scrape a LinkedIn profile."""

    logger.info(f"Received request to scrape: {request.linkedin_url}")

    scraped_data = scrape_linkedin_profile(request.linkedin_url)
    
    if "error" in scraped_data:
        raise HTTPException(status_code=500, detail=scraped_data["error"])

    return scraped_data

@router.post("/scrape_html", dependencies=[Depends(verify_api_key)])
async def scrape_profile_html(file: UploadFile = File(...)):
    """API endpoint to scrape a LinkedIn profile from an uploaded HTML file."""
    return scrape_linkedin_html(file)