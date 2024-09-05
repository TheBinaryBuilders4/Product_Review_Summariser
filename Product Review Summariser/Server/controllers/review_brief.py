from controllers.utils.ScrapperModule import Scrapper
from controllers.utils.classify_reviews import classify_reviews
from controllers.utils.summarise_reviews import summarise_reviews
from controllers.utils.getProductTitle import extract_product_name

scrapper = Scrapper()

async def review_brief(url: str):
    prodTitle = await extract_product_name(url)
    reviews =  await scrapper.scrap_reviews(url)
    classified_reviews = await classify_reviews(reviews)
    summarised_reviews = await summarise_reviews(classified_reviews, prodTitle)
    return summarised_reviews