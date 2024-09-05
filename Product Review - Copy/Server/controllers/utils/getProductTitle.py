from urllib.parse import urlparse

async def extract_product_name(url):
    try:
        # Parse the URL to get the path
        parsed_url = urlparse(url)
        path_segments = parsed_url.path.split('/')
        
        # Find the segment that contains the product name (usually the first one with hyphens)
        for segment in path_segments:
            if '-' in segment:
                # Replace hyphens with spaces and return the product name
                product_name = segment.replace('-', ' ')
                return product_name
        
        return "Product name not found"
    
    except Exception as e:
        return f"Error extracting product name: {e}"

