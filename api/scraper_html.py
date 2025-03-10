import logging
from bs4 import BeautifulSoup
from fastapi import UploadFile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def scrape_linkedin_html(file: UploadFile):
    """Parses LinkedIn profile data from an uploaded HTML file and extracts structured information."""
    try:
        logger.info("\n========================= 📥 STARTING HTML SCRAPE =========================")

        # Read and parse the HTML file
        html_content = file.file.read().decode("utf-8")
        soup = BeautifulSoup(html_content, "html.parser")
        logger.info("✅ Successfully loaded HTML file for scraping.")

        # Extract the Profile Name
        name = None
        title_tag = soup.select_one('span._name_1sdjqx p[data-anonymize="person-name"]')
        if title_tag:
            name = title_tag.text.strip()
        else:
            logger.warning("⚠️ Name not found in HTML file.")

        # Extract 'About' Section
        about = None
        about_section = soup.select_one('p[data-anonymize="headline"]')
        if about_section:
            about = about_section.text.strip()
        else:
            logger.warning("⚠️ About section not found.")

        # Extract Experiences
        experiences = []
        experience_sections = soup.select('li._experience-entry_1irc72')
        if experience_sections:
            for section in experience_sections:
                job_title = section.select_one('h2[data-anonymize="job-title"]')
                company_name = section.select_one('p[data-anonymize="company-name"]')
                duration = section.select_one('span.PrxiOvxgXUptgDlvHGSpEHbPmOrBVrebNtFdk')
                location = section.select_one('p.tThGMnUDqKUrDCiQEaUyRgZZWZCeudQ')
                description = section.select_one('div[data-anonymize="person-blurb"]')

                experiences.append({
                    "position_title": job_title.text.strip() if job_title else None,
                    "institution_name": company_name.text.strip() if company_name else None,
                    "duration": duration.text.strip() if duration else None,
                    "location": location.text.strip() if location else None,
                    "description": description.text.strip() if description else None
                })
            logger.info(f"✅ Extracted {len(experiences)} experience entries.")
        else:
            logger.warning("⚠️ No experience data found.")

        # Extract Education
        education = []
        education_section = soup.find("section", {"data-sn-view-name": "feature-lead-education"})
        if education_section:
            edu_items = education_section.find_all("li")
            for edu in edu_items:
                school_name = edu.find("h3").text.strip() if edu.find("h3") else None
                degree = edu.find("p").text.strip() if edu.find("p") else None
                
                # Extract years
                date_span = edu.find("time")
                start_year = date_span.text if date_span else None
                end_year = date_span.find_next("time").text if date_span and date_span.find_next("time") else None

                if school_name:
                    education.append({
                        "institution_name": school_name,
                        "degree": degree,
                        "start_year": start_year,
                        "end_year": end_year
                    })

            logger.info(f"✅ Extracted {len(education)} education entries.")
        else:
            logger.warning("⚠️ No education data found.")

        # Extract Profile Photo
        profile_photo = None
        profile_photo_tag = soup.find("img", {"data-anonymize": "headshot-photo"})
        if profile_photo_tag and "src" in profile_photo_tag.attrs:
            profile_photo = str(profile_photo_tag["src"])

            logger.info(f"✅ Extracted {len(profile_photo)} photo.")
        else:
            logger.warning("⚠️ No Profile Photo data found.")

        logger.info("========================= ✅ SCRAPE COMPLETED ✅ =========================")
        
        return {
            "name": name,
            "about": about,
            "experiences": experiences,
            "education": education,
            "profile_photo": profile_photo
        }

    except Exception as e:
        logger.error(f"❌ ERROR DURING SCRAPING: {e}", exc_info=True)
        return None