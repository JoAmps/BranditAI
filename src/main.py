from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from data.scraper.website_scraper import WebsiteScraper
from models.open_ai import OpenAIHandler

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/scrape_website")
async def scrape_website(request_data: dict):

    url = request_data.get("url")

    html = WebsiteScraper().access_html_of_url(url)
    model = OpenAIHandler()

    scraped_output = await WebsiteScraper().scraper(html, model)
    brand_summary = await model.summarize_brand_website(scraped_output)
    one_liner = await model.generate_one_liner(brand_summary)
    return scraped_output, brand_summary, one_liner


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
