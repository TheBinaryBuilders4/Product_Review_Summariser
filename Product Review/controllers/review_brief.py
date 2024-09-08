from controllers.utils.ScrapperModule import Scrapper
from controllers.utils.ClassificationModule import ClassificationModule
from controllers.utils.summarise_reviews import summarise_reviews

scrapper = Scrapper()
classifier = ClassificationModule()

async def review_brief(url: str):
    prodTitle = await scrapper.extract_product_name(url)
    reviews =  await scrapper.scrap_reviews(url)
    classified_reviews = await classifier.classify_reviews(reviews)
    summarised_reviews = await summarise_reviews(classified_reviews, prodTitle)
    return summarised_reviews