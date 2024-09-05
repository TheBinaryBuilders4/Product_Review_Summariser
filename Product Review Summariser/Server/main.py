from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

import os

from models.ProductUrl import ProductUrl
from controllers.review_brief import review_brief

app = FastAPI()

# CORS middleware
# cross origin resource sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/getReviews/")
async def summarise(data: ProductUrl):
    return await review_brief(data.url)


if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 8000))  # Retrieve PORT or default to 4000
    except ValueError:  # Handle invalid PORT values
        print("Invalid PORT environment variable. Using default port 4000.")
        port = 4000
    
    try:
        run(app, host="127.0.0.1", port=port)
    except Exception as e:
        print(f"Error: {e}")
        print("Exiting...")
        exit(1)
    
