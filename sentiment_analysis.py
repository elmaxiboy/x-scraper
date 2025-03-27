import json
import logging 
from transformers import TextClassificationPipeline, AutoModelForSequenceClassification, AutoTokenizer,BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import torch

logging.basicConfig(level=logging.INFO)

OUTPUT_NAME= "results/scraped_tweets_with_sentiment.json"

def sentiment_analysis(input_file):

    try:


        #Load scrapped tweets
        tweets = []

        with open(input_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        for tweet in data:
            tweets.append(tweet["tweet"]["content"])


        #roBERTa model (for base sentiment)
        #https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment

        # Load model and tokenizer
        model_name = "cardiffnlp/twitter-roberta-base-sentiment"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)

        # Define labels (specific to this model)
        labels = ["negative", "neutral", "positive"]

        def preprocess_tweets(tweets):
            return tokenizer(tweets, padding=True, truncation=True, return_tensors="pt")

        # Tokenize tweets
        inputs = preprocess_tweets(tweets)

        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

        #Assign predictions
        for tweet, prediction in zip(data, predictions):
            tweet["tweet"]["base_sentiment"]= {
                "label": (labels[prediction.argmax().item()]).lower(),
                "score": prediction.max().item()
            }

        #cryptoBERT model for risk tagging 
        #https://huggingface.co/ElKulako/cryptobert

        model_name = "ElKulako/cryptobert"
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels = 3)
        pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, max_length=64, truncation=True, padding = 'max_length')

        #Assign predictions
        predicted_labels = pipe(tweets)
        for tweet, label in zip(data, predicted_labels):
            tweet["tweet"]["risk_sentiment"]={
                "label" : label["label"].lower(),
                "score" : label["score"]
            }


        #Crypto Market Sentiment (fine-tuned version of finBERT)
        #https://huggingface.co/kk08/CryptoBERT

        tokenizer = BertTokenizer.from_pretrained("kk08/CryptoBERT")
        model = BertForSequenceClassification.from_pretrained("kk08/CryptoBERT")

        classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
        predicted_labels = classifier(tweets)
        for tweet, label in zip(data, predicted_labels):
            if label=="LABEL_1":
                tweet["tweet"]["crypto_sentiment"]={
                    "label" : "positive",
                    "score" : label["score"]
                    } 
            tweet["tweet"]["sentiment-finBERT"]={
                "label" : "negative",
                "score" : label["score"]
                } 

    except Exception as e:
         logging.error(f"Error while performing sentiment analysis: {e}")

    except KeyboardInterrupt:
        logging.warning("Process interrupted by the user!")
        exit(1)      
    finally:
        with open(OUTPUT_NAME, "w", encoding="utf-8") as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=4)
        logging.info(f"Sentiment analysis ended. Results saved into {OUTPUT_NAME}")


           