from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from data.scraper.website_scraper import WebsiteScraper
from models.open_ai import OpenAIHandler
from aws.aws_cloud import AWSHandler
from helper_functions import HelperFunctions

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
    company_name = request_data.get("company_name")

    aws = AWSHandler()

    bucket_name = HelperFunctions.bucket_name(company_name)
    aws.create_s3_bucket(bucket_name)

    html = WebsiteScraper().access_html_of_url(url)
    model = OpenAIHandler()

    scraped_output = await WebsiteScraper().scraper(html, model)
    aws.upload_string_to_s3(bucket_name, "scraped_output.txt", scraped_output)
    brand_summary = await model.summarize_brand_website(scraped_output)
    aws.upload_string_to_s3(bucket_name, "brand_summary.txt", brand_summary)
    one_liner = await model.generate_one_liner(brand_summary)
    aws.upload_string_to_s3(bucket_name, "one_liner.txt", one_liner)

    return {
        "scraped_data": scraped_output,
        "brand_summary": brand_summary,
        "one_liner": one_liner,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
