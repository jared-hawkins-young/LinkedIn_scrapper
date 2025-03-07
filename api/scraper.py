import os
import logging
import json
from dotenv import load_dotenv
from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
load_dotenv()

# Configure logging format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def scrape_linkedin_profile(linkedin_url):
    """Scrapes a LinkedIn profile and returns raw data as JSON with improved logging."""
    try:
        logger.info("\n========================= 🔍 STARTING LINKEDIN SCRAPE =========================")
        logger.info(f"🔗 Target Profile: {linkedin_url}")

        # Set up Selenium WebDriver
        logger.info("\n📢 [STEP 1] Setting up Chrome WebDriver...")
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        driver = webdriver.Chrome(service=service, options=options)
        logger.info("✅ WebDriver successfully initialized.")

        # Load credentials from .env
        email = os.getenv("LINKEDIN_USER")
        password = os.getenv("LINKEDIN_PASSWORD")

        if not email or not password:
            logger.error("❌ ERROR: Missing LinkedIn credentials in .env file.")
            raise ValueError("LinkedIn credentials are not set in .env file.")

        # Log in to LinkedIn
        logger.info(f"\n📢 [STEP 2] Logging into LinkedIn as: {email}")
        actions.login(driver, email, password)
        logger.info("✅ Login successful.")

        # Scrape profile
        logger.info("\n📢 [STEP 3] Scraping LinkedIn profile...")
        person = Person(linkedin_url, driver=driver)
        logger.info(f"✅ Successfully scraped profile: {linkedin_url}")

        # Convert scraped data to dictionary
        logger.info("\n📢 [STEP 4] Converting scraped data to JSON...")
        person_data = {
            "name": person.name,
            "about": person.about,
            "experiences": [exp.__dict__ for exp in person.experiences],
            "education": [edu.__dict__ for edu in person.educations],
            "company": person.company,
            "job_title": person.job_title,
            "interests": getattr(person, "interests", None), 
            "accomplishments": getattr(person, "accomplishments", None)
        }
        logger.info("✅ Data conversion successful.")

        # Close WebDriver
        driver.quit()
        logger.info("\n📢 [STEP 5] Closing WebDriver...")
        logger.info("✅ WebDriver closed successfully.")

        logger.info("\n========================= ✅ SCRAPE COMPLETE =========================\n")
        return person_data

    except Exception as e:
        logger.error("\n❌ ERROR: Scraping failed!")
        logger.exception(f"🔴 Exception Details: {e}")
        return {"error": str(e)}