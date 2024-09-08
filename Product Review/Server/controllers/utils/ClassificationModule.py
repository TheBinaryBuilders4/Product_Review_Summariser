import torch
from transformers import AutoTokenizer
from ML_models.TextModel import CONFIG, TextModel

class ClassificationModule():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(CONFIG['model_name'])
        self.model = TextModel(CONFIG['model_name'])
        self.model.load_state_dict(torch.load("ML_models/Loss-Fold-2.bin", map_location=CONFIG['device']))
        self.model.to(CONFIG['device'])
        self.model.eval()
        

    def predict_sentiment(self, texts):
        # Tokenize the input texts
        inputs = self.tokenizer(texts, padding=True, truncation=True, max_length=CONFIG['max_length'], return_tensors="pt")
        input_ids = inputs['input_ids'].to(CONFIG['device'])
        attention_mask = inputs['attention_mask'].to(CONFIG['device'])
        
        # Forward pass through the model
        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask)
            logits = outputs
            predictions = torch.argmax(logits, dim=1)
        
        return predictions


    async def classify_reviews(self, reviews):
        print("Classifying reviews...")
        # Predict the sentiment of the input texts
        predictions = self.predict_sentiment(reviews)

        # class_labels = ["Negative", "Neutral", "Positive"]

        classified_reviews = {
            "Negative": [],
            "Neutral": [],
            "Positive": []
        }

        # Convert indices to labels
        def interpret_predictions(predictions):
            for review, prediction in zip(reviews, predictions):
                if prediction == 0:
                    classified_reviews["Negative"].append(review)
                elif prediction == 1:
                    classified_reviews["Neutral"].append(review)
                else:
                    classified_reviews["Positive"].append(review)
            return None
        

        interpret_predictions(predictions)
        
        print(f'''
    Successfully classified reviews into Positive, Negative and Neutral:
    Positive Reviews: {len(classified_reviews['Positive'])}
    Neutral Reviews: {len(classified_reviews['Neutral'])}
    Negative Reviews: {len(classified_reviews['Negative'])}
            \n''')
        
        return classified_reviews