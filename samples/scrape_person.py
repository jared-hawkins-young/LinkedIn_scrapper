import os
from dotenv import load_dotenv
from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json

load_dotenv()

# Auto-download the correct ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

email = os.getenv("LINKEDIN_USER")
password = os.getenv("LINKEDIN_PASSWORD")
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
person = Person("https://www.linkedin.com/in/alexbuckles/", driver=driver)

# Convert scraped data to dictionary
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

# Pretty print the raw scraped data
print(json.dumps(person_data, indent=4, ensure_ascii=False))

