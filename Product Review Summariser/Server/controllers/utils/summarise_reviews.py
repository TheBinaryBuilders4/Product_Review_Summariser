import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv() 

def brief_summary(reviews):
    return "\n".join(reviews[:5])

async def summarise_reviews(classified_reviews, prodTitle):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    print("Summarising reviews...\n")
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f''' 
                    *Here are the product reviews classified into Positive, Negative and Neutral:*
                    Positive Reviews:
                    {brief_summary(classified_reviews['Positive'])}
                    Negative Reviews: 
                    {brief_summary(classified_reviews['Negative'])}
                    Neutral Reviews: 
                    {brief_summary(classified_reviews['Neutral'])}
                    Prod Title:
                    {prodTitle}
                    
                    *USING THESE GIVE ONLY AND ONLY 6 PROS AND 6 CONS OF THE PRODUCT IN BULLET POINTS*
                    *ALSO USING ALL THE REVIEWS, GIVE A BRIEF SUMMARY OF THE PRODUCT IN 3-4 LINES*

                    Below is an example of the exact format of the response, which should be followed.
                    Don't change the format of the response, just replace the content with the actual reviews and summary. Each pros and cons should be 8 to 15 words.
                    Return nothing extra, just the response in the exact format as shown below.
                    In place of prodTitle generate a shortened title from the given long product title.
                    Also add a key-value array where the key is a string representing the feature name (e.g., 'Speed', 'Durability'), and the value is a numeric rating out of 5. and give the respose like 'Durability' : 4.0, 'Speed' : 5.0
                    
                    PROS and CONS should not be conflicting with each other. If a PRO is mentioned in the CONS, it should be removed from the CONS.
            
                    Here is an example of the expected format:
                    {{
                        "pros": [
                            "Good quality for the price: Offers solid value without breaking the bank.",
                            "Decent comfort level: Comfortable for extended periods of sitting.",
                            "Adjustable features: Customizable settings for different user preferences"
                        ],
                        "cons": [
                            "Poor quality control: Inconsistent manufacturing leads to varying product quality.",
                            "Flimsy construction: Weak materials make the chair less durable overall."
                        ],
                        "summary": "The product is a decent chair with good quality for the price, decent comfort level, adjustable features, easy to assemble, and good for the money. However, it has some significant drawbacks including poor quality control, flimsy construction, armrests that loosen frequently, backrest that wears down quickly, and roaches found in the box.",
                        "prodTitle" : "Mi Xiaomi X Pro 43\" 4K QLED TV",
                        "features":[]
                    }}

                    STRICTLY MAINTAIN THE FORMAT AS SHOWN ABOVE
                    ''',
                }
            ],
            model="llama3-8b-8192",
        )
    except Exception as e:
        print(f"Error: {e}")
        return None
    # print('response', response.choices[0].message.content)

    # Initialize variables to store parsed data
    pros, cons, summary, productTitle = [], [], "", ""
    parsed_data = {}
    
    # Extract and parse response content
    try:
        content = response.choices[0].message.content
        start_index = content.find('{')
        end_index = content.rfind('}') + 1
        
        if start_index != -1 and end_index != -1:
            json_content = content[start_index:end_index]
            parsed_data = json.loads(json_content)
            
            pros = parsed_data.get('pros', [])
            cons = parsed_data.get('cons', [])
            summary = parsed_data.get('summary', '')
            productTitle = parsed_data.get('prodTitle')
            
            # Ensure pros and cons are in correct format
            pros = [p.strip() for p in pros]
            cons = [c.strip() for c in cons]
            
            # Log lengths to verify if they are as expected
            print(f"Pros: {len(pros)}, Cons: {len(cons)}, Summary Length: {len(summary)}")
    
    except json.JSONDecodeError:
        print("Failed to decode JSON from the response.")
    except Exception as e:
        print(f"Error during parsing: {e}")

    summarised_reviews = {
        'pros': pros[:6],
        'cons': cons[:6],  
        'summary': summary,
        'prodTitle': productTitle,
        'features': parsed_data.get('features', []),  
        'Positive': len(classified_reviews['Positive']),  
        'Negative': len(classified_reviews['Negative']),  
        'Neutral' : len(classified_reviews['Neutral']),  
    }
    
    # Log and return the final result
    print(summarised_reviews)
    print("\nSummarised reviews successfully!\n")
    return summarised_reviews
