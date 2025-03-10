# LinkedIn Scraper API

## Installation
Ensure you have Python installed, then install dependencies:
```sh
pip install -r requirements.txt
```

## Running the API
Start the FastAPI server with:
```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Authentication
All requests must include the secret key in the headers:
```sh
Authorization: Bearer sk_3xMPL3S3Cr3tK3Y12345
```

## Endpoints

### Health Check
**GET /**
Checks if the service is running.
#### Response:
```json
{
  "status": "healthy"
}
```

### Scrape Profile
**POST /scrape**
Scrapes a LinkedIn profile from a provided URL.
#### Request Body:
```json
{
  "linkedin_url": "https://www.linkedin.com/in/example-profile"
}
```
#### Response:
```json
{
  "name": "John Doe",
  "about": "Experienced Software Engineer...",
  "experiences": [
    {
      "position_title": "Software Engineer",
      "institution_name": "Tech Company",
      "duration": "Jan 2020 - Present",
      "description": "Developing scalable applications..."
    }
  ],
  "education": []
}
```

### Scrape Profile from HTML
**POST /scrape_html**
Scrapes a LinkedIn profile from an uploaded HTML file.
#### Request:
- Upload HTML file as `multipart/form-data`

#### Response:
```json
{
  "name": "Jane Doe",
  "about": "Marketing Specialist...",
  "experiences": [
    {
      "position_title": "Marketing Manager",
      "institution_name": "Media Corp",
      "duration": "Feb 2018 - Present",
      "description": "Managing brand strategy..."
    }
  ],
  "education": []
}