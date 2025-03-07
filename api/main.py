from fastapi import FastAPI
from routes import router

app = FastAPI(title="LinkedIn Scraper API")

# Include API routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)